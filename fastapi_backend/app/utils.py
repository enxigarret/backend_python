
from app.core.config import settings
import emails
import logging  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    

def send_email(*, email_to: str, subject: str, html_content: str) -> None:
    """
    Send an email.
    """
    # Implement your email sending logic here using your preferred email library
    assert settings.emails_enabled, "Emails are not enabled. Set settings.emails_enabled to True to enable email sending."
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.EMAILS_SMTP_HOST, "port": settings.EMAILS_SMTP_PORT}
    if settings.EMAILS_SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.EMAILS_SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.EMAILS_SMTP_USER:
        smtp_options["user"] = settings.EMAILS_SMTP_USER
    if settings.EMAILS_SMTP_PASSWORD:
        smtp_options["password"] = settings.EMAILS_SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    logger.info(f"Sent email to {email_to}: {response}")



def generate_new_account_email(*, email_to: str, username: str, password: str) -> emails.Message:
    """
    Generate email for account creation.
    """
    subject = "Your new account has been created"
    html_content = f"""
    <p>Hi {username},</p>
    <p>Your new account has been created successfully. Here are your login details:</p>
    <ul>
        <li><strong>Email:</strong> {email_to}</li>
        <li><strong>Password:</strong> {password}</li>
    </ul>
    <p>Please keep this information secure and do not share it with anyone.</p>
    <p>Best regards,<br>Your Company Team</p>
    """
    return emails.Message(subject=subject, html=html_content)
