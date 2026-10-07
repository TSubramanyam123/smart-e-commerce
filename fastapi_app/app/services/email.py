import logging
import smtplib

from email.message import EmailMessage

from app.core.config import settings


logger = logging.getLogger(__name__)


def send_email(
    to_email: str,
    subject: str,
    body: str
):

    if not settings.smtp_host:

        logger.info(
            "SMTP is not configured. "
            "Email would be sent to %s: %s",
            to_email,
            body
        )

        return

    message = EmailMessage()

    message["From"] = (
        settings.smtp_from_email
    )

    message["To"] = to_email

    message["Subject"] = subject

    message.set_content(body)

    with smtplib.SMTP(
        settings.smtp_host,
        settings.smtp_port
    ) as smtp:

        if settings.smtp_use_tls:

            smtp.starttls()

        if settings.smtp_username:

            smtp.login(
                settings.smtp_username,
                settings.smtp_password
            )

        smtp.send_message(message)