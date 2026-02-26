
import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, Depends
from app.core.config import settings
from sqlmodel import col ,delete, select,func

from app import crud

from  app.api.deps import SessionDep, get_current_active_superuser
from app.models import UserCreate, User, UserPublic , UserRegister

from app.utils import generate_new_account_email, send_email

router = APIRouter(prefix="/users", tags=["users"])

@router.get(
        "/",
        dependencies=[Depends(get_current_active_superuser)], 
        response_model=list[UserPublic])

def read_users(
    *,
    session: SessionDep,
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve users.
    """
    statement = select(User).offset(skip).limit(limit)
    count = session.exec(select([col(func.count())]).select_from(User)).scalar_one()
    users = session.exec(statement).all()
    return UserPublic(data=users,cout=count)


@router.post(
    "/", 
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic, 
    status_code=201)

def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        ) 

    user = crud.create_user(session=session, user_create=user_in)
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user

@router.post("/signup", 
             response_model=UserPublic, 
             status_code=201)
def register_user(session:SessionDep,user_in:UserRegister)->Any:
    """
    Create new user without the need to be logged in.
    """
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user_create = UserCreate.model_calidate(user_in )
    user = crud.create_user(session=session, user_create=user_create)
    return user

# @router.post("/signup", response_model=UserRead, status_code=201) 
# def  register_user(
#     *,
#     session: SessionDep,
#     user_in: UserRegister,
# ) -> Any:
#     """
#     Create new user without the need to be logged in.
#     """
#     user = crud.get_user_by_email(session=session, email=user_in.email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this email already exists in the system.",
#         )
#     user_create = UserCreate.model_calidate(user_in )
#     user = crud.create_user(session=session, user_create=user_create)
#     return user