from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from sqlalchemy import DateTime 

from datetime import datetime
import uuid


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True,max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserUpdate(SQLModel):
    password: str | None = Field(default=None, min_length=8, max_length=128)
    email:EmailStr | None = Field(unique=True, index=True,max_length=255)

class User(UserBase, table=True):
    id: uuid.UUID  = Field( default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(default_factory=datetime.utcnow)

class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None
    
class UserRegister(SQLModel):
    email: EmailStr = Field(unique=True, index=True,max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)

    # JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)