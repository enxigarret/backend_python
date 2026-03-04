
import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, Depends
from app.core.config import settings
from sqlmodel import col ,delete, select,func

from app import crud

from  app.api.deps import SessionDep, get_current_active_superuser
from app.models import UserCreate, User, UserPublic , UserRegister,UserInDB,UserUpdate

from app.utils import generate_new_account_email, send_email

router = APIRouter(tags=["users"])

@router.get(
        "/",
        dependencies=[Depends(get_current_active_superuser)], 
        response_model=UserInDB)

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
    count_stmt = select(func.count()).select_from(User)
    count = session.exec(count_stmt).one()
    users = session.exec(statement).all()
    return UserInDB(data=users,count=count)


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
    user_create = UserCreate.model_validate(user_in )
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

@router.get(
        "/{user_id}", 
        response_model=UserPublic, 
        dependencies=[Depends(get_current_active_superuser)])
def get_user(
    *,
    session: SessionDep,
    user_id: uuid.UUID
) -> Any:
    """
    Get user by ID.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch(
    "/{id}", 
    response_model=UserPublic, 
    dependencies=[Depends(get_current_active_superuser)])
def update_user(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    user_in:UserUpdate)-> Any:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_in.email and user_in.email != db_user.email:
        existing_user = crud.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:   
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )
    user_data = crud.update_user(session=session, db_user=db_user, user_update=user_in)
    return user_data


    