import uuid
from typing import Any

from sqlmodel import SQLModel, Session, select
from app.models import User,UserCreate, UserUpdate

from app.core.security import get_password_hash, verify_password

def create_user(*,session: Session,user_create:UserCreate) -> User:
    db_user_obj = User.model_validate(
        user_create, 
        update ={"hashed_password":  get_password_hash(user_create.password )}
    )
  
    session.add(db_user_obj)
    session.commit()
    session.refresh(db_user_obj)
    return db_user_obj

def updatate_user(*,session: Session, db_user: User, user_update: UserUpdate) -> Any:
    user_data = user_update.model_dump(exclude_unset=True)

    extra_data = {}
    if "passward" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
        
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first
    return session_user

# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"

def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        # Perform a dummy hash verification to mitigate timing attacks
        verify_password(password, DUMMY_HASH)
        return None
    verified, updatate_password_hash= verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    if updatate_password_hash:
        db_user.hashed_password = updatate_password_hash
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user
