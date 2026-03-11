from celery import shared_task
from datetime import date, timedelta
from flask import current_app
from mail import send_email


# ---------------------------------------------------------------------------
# a. Scheduled Job – Daily Reminders
# ---------------------------------------------------------------------------

@shared_task(name="tasks.mail_tasks.send_daily_reminders")
def send_daily_reminders():
    """
    Runs daily. Sends reminder emails to students who have applied to drives
    whose application deadline is within the next 3 days.
    Also reminds students about approved drives they haven't applied to yet.
    """
    from model import Application, PlacementDrive, Student, User, Company

    today = date.today()
    warning_date = today + timedelta(days=3) #drive deadline in 3 days

    # Drives with deadlines approaching in the next 3 days (still open)
    upcoming_drives = PlacementDrive.query.filter(
        PlacementDrive.status == "approved",
        PlacementDrive.application_deadline >= today,
        PlacementDrive.application_deadline <= warning_date,
    ).all()

    if not upcoming_drives:
        return "No upcoming deadlines – no reminders sent."

    sent_count = 0
    for drive in upcoming_drives:
        # Find all active students who have NOT yet applied to this drive
        applied_student_ids = {
            a.student_id
            for a in Application.query.filter_by(drive_id=drive.id).all()
        }

        eligible_students = Student.query.filter_by(is_active=True).all()
        for student in eligible_students:
            if student.id in applied_student_ids:
                continue  # already applied

            user = User.query.get(student.user_id)
            if not user or not user.email:
                continue

            days_left = (drive.application_deadline - today).days
            company = Company.query.get(drive.company_id)
            company_name = company.company_name if company else "Unknown"

            subject = f"Reminder: {drive.drive_name} deadline in {days_left} day(s)"
            html = f"""
            <html><body>
            <h2>Placement Drive Deadline Reminder</h2>
            <p>Dear {student.name or user.name},</p>
            <p>
                This is a reminder that the application deadline for
                <strong>{drive.drive_name}</strong> by <strong>{company_name}</strong>
                is on <strong>{drive.application_deadline}</strong>
                — that is <strong>{days_left} day(s)</strong> from today.
            </p>
            <p>
                <b>Job Title:</b> {drive.job_title}<br>
                <b>Salary:</b> {drive.salary}<br>
                <b>Deadline:</b> {drive.application_deadline}
            </p>
            <p>Log in to the placement portal and apply before the deadline!</p>
            <br>
            <p>Best regards,<br>Placement Portal Team</p>
            </body></html>
            """
            try:
                send_email(user.email, subject, html)
                sent_count += 1
            except Exception as e:
                current_app.logger.error(
                    f"Failed to send reminder to {user.email}: {e}"
                )

    return f"Daily reminders sent: {sent_count}"


# ---------------------------------------------------------------------------
# b. Scheduled Job – Monthly Activity Report
# ---------------------------------------------------------------------------

@shared_task(name="tasks.mail_tasks.send_monthly_report")
def send_monthly_report():
    """
    Runs on the 1st of every month. Sends an HTML activity report to the admin.
    """
    from model import PlacementDrive, Application, User
    from datetime import datetime

    today = date.today()
    # Report covers the previous month
    first_of_this_month = today.replace(day=1)
    last_month_end = first_of_this_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    # Drives approved / created last month
    drives = PlacementDrive.query.filter(
        PlacementDrive.created_at >= datetime.combine(last_month_start, datetime.min.time()),
        PlacementDrive.created_at < datetime.combine(first_of_this_month, datetime.min.time()),
    ).all()

    # Applications submitted last month
    applications = Application.query.filter(
        Application.applied_date >= last_month_start,
        Application.applied_date < first_of_this_month,
    ).all()

    total_drives = len(drives)
    total_applied = len(applications)
    total_selected = sum(1 for a in applications if a.status == "selected")

    # Build drive rows HTML
    drive_rows = ""
    for d in drives:
        drive_rows += f"<tr><td>{d.id}</td><td>{d.drive_name}</td><td>{d.job_title}</td><td>{d.status}</td><td>{d.application_deadline}</td></tr>"

    html = f"""
    <html><body style="font-family: Arial, sans-serif; color: #333;">
    <h1 style="color:#2c3e50;">Monthly Placement Activity Report</h1>
    <h3>Period: {last_month_start.strftime('%B %Y')}</h3>

    <table style="border-collapse:collapse; margin-bottom:20px;">
        <tr>
            <td style="padding:10px 20px; background:#3498db; color:#fff; border-radius:4px;">
                <strong>Drives Conducted</strong><br><span style="font-size:2em;">{total_drives}</span>
            </td>
            <td style="padding:10px 20px; background:#2ecc71; color:#fff; border-radius:4px; margin-left:10px;">
                <strong>Students Applied</strong><br><span style="font-size:2em;">{total_applied}</span>
            </td>
            <td style="padding:10px 20px; background:#e74c3c; color:#fff; border-radius:4px; margin-left:10px;">
                <strong>Students Selected</strong><br><span style="font-size:2em;">{total_selected}</span>
            </td>
        </tr>
    </table>

    <h2>Drives This Month</h2>
    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse; width:100%;">
        <thead style="background:#ecf0f1;">
            <tr>
                <th>ID</th><th>Drive Name</th><th>Job Title</th><th>Status</th><th>Deadline</th>
            </tr>
        </thead>
        <tbody>
            {drive_rows if drive_rows else '<tr><td colspan="5" style="text-align:center;">No drives this month</td></tr>'}
        </tbody>
    </table>

    <br>
    <p style="color:#7f8c8d; font-size:0.9em;">
        Generated on {today.strftime('%d %B %Y')} by Placement Portal
    </p>
    </body></html>
    """

    admin_email = current_app.config.get("ADMIN_EMAIL")
    if not admin_email:
        return "ADMIN_EMAIL not configured – report not sent."

    try:
        send_email(
            admin_email,
            f"Monthly Placement Report – {last_month_start.strftime('%B %Y')}",
            html,
        )
        return f"Monthly report sent to {admin_email}"
    except Exception as e:
        current_app.logger.error(f"Failed to send monthly report: {e}")
        return f"Error sending monthly report: {e}"
