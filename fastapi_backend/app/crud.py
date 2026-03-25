from typing import Any

from sqlmodel import Session

from app.adapters.password_hasher_pwdlib import PwdlibPasswordHasher
from app.adapters.user_repository_sqlmodel import SqlModelUserRepository
from app.models import User, UserCreate, UserUpdate
from app.services.user_service import UserService


def _build_user_service(session: Session) -> UserService:
    return UserService(
        user_repository=SqlModelUserRepository(session),
        password_hasher=PwdlibPasswordHasher(),
    )


def create_user(*, session: Session, user_create: UserCreate) -> User:
    return _build_user_service(session).create_user(user_create)


def update_user(*, session: Session, db_user: User, user_update: UserUpdate) -> Any:
    return _build_user_service(session).update_user(db_user, user_update)


def get_user_by_email(*, session: Session, email: str) -> User | None:
    return _build_user_service(session).get_user_by_email(email)


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    return _build_user_service(session).authenticate(email=email, password=password)

