
from app.core.config import settings
import emails
import logging  
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    
from pathlib import Path
from jinja2 import Template
from typing import Any
import jwt
import app.core.security as security
from datatime import timedelta, timezone, datetime


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content

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
    subject = f"Your new account has been created, for new account with username: {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={"username": username, "password": password,"email_to": email_to},
    )
    return emails.Message(subject=subject, html=html_content)

def verify_password_reset_token(*, token: str) -> str:  
    """
    Verify password reset token and return email if valid.
    """
    # Implement your token verification logic here
    # For example, decode the token and extract the email
    # If the token is invalid or expired, raise an appropriate exception
    try:
        decoded_token = jwt.decode(
        token,
        settings.SECRET_KEY, 
        algorithms=[security.ALGORITHM]
    )
        return str(decoded_token.get("sub"))

    except:
        NotImplementedError("Password reset token verification is not implemented yet.")
        return None
    
def generate_password_reset_token(email:str) -> str:
    """
    Generate a password reset token for the given email.
    """
    # Implement your token generation logic here
    # For example, create a JWT token with the email as the subject and an expiration time
    delta= timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)  # Token valid for 1 hour
    now = datetime.now(timezone=timezone.utc)
    expires = now+delta
    exp = expires.timestamp()
    try:
        token = jwt.encode(
            {"exp": exp, "nbf": now, "sub": email},    
            settings.SECRET_KEY,
            algorithm=security.ALGORITHM
        )
        return token
    except:
        NotImplementedError("Password reset token generation is not implemented yet.")
        return None

