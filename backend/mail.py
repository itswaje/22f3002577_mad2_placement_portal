import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
FROM_EMAIL = 'admin@placementportal.com'


def send_email(to_email, subject, body):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.send_message(msg)
    print(f"Email sent to {to_email}")


def send_email_with_attachment(to_email, subject, body, filename, file_data):
    """Send an HTML email with a file attachment via MailHog."""
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    msg.attach(MIMEText(body, 'html'))

    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(file_data)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(attachment)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.send_message(msg)
    print(f"Email with attachment sent to {to_email}")
