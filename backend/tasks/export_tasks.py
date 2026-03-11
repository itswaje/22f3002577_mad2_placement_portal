import csv
import io
from celery import shared_task
from flask import current_app
from mail import send_email, send_email_with_attachment


@shared_task(bind=True, name="tasks.export_tasks.export_applications_csv")
def export_applications_csv(self, student_id):
    """
    Async job: Exports all applications for a student as a CSV attachment
    and emails it to the student.
    """
    from model import Application, PlacementDrive, Company, Student, User

    student = Student.query.get(student_id)
    if not student:
        return {"status": "error", "message": "Student not found"}

    user = User.query.get(student.user_id)
    if not user:
        return {"status": "error", "message": "User not found"}

    applications = Application.query.filter_by(student_id=student_id).all()

    # Build CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Student ID",
        "Student Name",
        "Company Name",
        "Drive Title",
        "Job Title",
        "Application Status",
        "Applied Date",
        "Application Deadline",
        "Drive Status",
    ])

    for app in applications:
        drive = PlacementDrive.query.get(app.drive_id)
        company = Company.query.get(drive.company_id) if drive else None
        writer.writerow([
            student.id,
            student.name or user.name,
            company.company_name if company else "N/A",
            drive.drive_name if drive else "N/A",
            drive.job_title if drive else "N/A",
            app.status,
            app.applied_date,
            drive.application_deadline if drive else "N/A",
            drive.status if drive else "N/A",
        ])

    csv_bytes = output.getvalue().encode("utf-8")
    output.close()

    subject = "Your Placement Application History - Export Ready"
    body_html = f"""
    <html><body>
    <h2>Application History Export</h2>
    <p>Dear {student.name or user.name},</p>
    <p>
        Your placement application history has been exported successfully.
        Please find the CSV file attached to this email.
    </p>
    <p><b>Total applications exported:</b> {len(applications)}</p>
    <br>
    <p>Best regards,<br>Placement Portal Team</p>
    </body></html>
    """

    try:
        send_email_with_attachment(
            user.email,
            subject,
            body_html,
            f"applications_student_{student_id}.csv",
            csv_bytes,
        )
        return {
            "status": "success",
            "message": f"CSV export sent to {user.email}",
            "total": len(applications),
        }
    except Exception as e:
        current_app.logger.error(f"Failed to send CSV export to {user.email}: {e}")
        return {"status": "error", "message": str(e)}
