
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated, Any
from app import crud
from app.core import security

from app.core.config import settings    
from app.api.deps import SessionDep, CurrentUser
from app.models import Token, UserPublic, NewPassword, UserUpdate, Message
import logging
from  app.utils import send_email, verify_password_reset_token,generate_password_reset_token, generate_password_reset_email



router = APIRouter(tags=["login"])

@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
)-> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    logging.info(f"Login attempt for email: {form_data.username}")
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return Token(
        access_token = security.create_access_token(user.id,expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    )

@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user

@router.post("/login/password-reset")
def reset_password(session:SessionDep, body:NewPassword) -> Any:
    """
    Password reset
    """
    email = verify_password_reset_token(token = body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.get_user_by_email(session=session, email=email)
    if not user:
        # do not reveal that the email does not exist
        raise HTTPException(status_code=404, detail="Invalid token")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    user_in_update = UserUpdate(password=body.new_password)
    crud.update_user(session=session, db_user=user, user_in=user_in_update)
    return Message(message="Password reset successful")

@router.post("/password-recovery/{email}")
def recover_password(session:SessionDep, email:str) -> Message:
    """
    Password recovery
    """
    user = crud.get_user_by_email(session=session, email=email)
    if user and user.is_active:
        password_reset_token = generate_password_reset_token(email=email)

        # send email with password reset token
        email_data = generate_password_reset_email(
            email_to=email, token=password_reset_token, email=email
        )
        send_email(
            email_to=email,           
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return Message(message="Password recovery email sent")