from decouple import config
from typing import Optional
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from fastapi import HTTPException, status
from fastapi.background import BackgroundTasks
from src.core.settings import get_settings

settings = get_settings()

def service_email(receiver_email: str, subject: str, html_content: str, attachment: Optional[bytes] = None, attachment_filename: Optional[str] = None):
    """
    Generic function to send an email

    Args:
        receiver_email (str): Email address of the receiver
        subject (str): Subject of the email
        body (str): Body of the email
        attachment (bytes, optional): Attachment file content
        attachment_filename (str, optional): Attachment filename

    Returns:
        bool: True if the email was sent successfully, False otherwise
    """
    msg = MIMEMultipart()
    msg['From'] = settings.SMTP_USER
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))
    if attachment and attachment_filename:
        attachment_part = MIMEBase('application', 'octet-stream')
        attachment_part.set_payload(attachment)
        encoders.encode_base64(attachment_part)
        attachment_part.add_header(
            'Content-Disposition', f'attachment; filename={attachment_filename}')
        msg.attach(attachment_part)
    try:
        if settings.SMTP_TLS:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()
        elif settings.SMTP_SSL:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)

        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.SMTP_USER, receiver_email, text)
        server.quit()
    except smtplib.SMTPException as e:
        print(f"SMTP Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="El correo no pudo ser enviado")
    except Exception as e:
        print(f"Unknown Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="El correo no pudo ser enviado")


def send_email(receiver_email: str, subject: str, html_content: str, attachment: Optional[bytes] = None, attachment_filename: Optional[str] = None, background_tasks: BackgroundTasks = None):
    """
    Send an email using a background task

    Args:
        receiver_email (str): Email address of the receiver
        subject (str): Subject of the email
        body (str): Body of the email
        attachment (bytes, optional): Attachment file content
        attachment_filename (str, optional): Attachment filename
        background_tasks (BackgroundTasks, optional): BackgroundTasks. Defaults to None.
    """
    if background_tasks:
        background_tasks.add_task(service_email, receiver_email,
                                  subject, html_content, attachment, attachment_filename)
    else:
        service_email(receiver_email, subject, html_content,
                      attachment, attachment_filename)