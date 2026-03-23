from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from sqlalchemy import DateTime 

from datetime import datetime, timezone
import uuid

def get_datetime_utc()-> datetime:
    return datetime.now(timezone.utc)
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
    
class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr|None = Field(unique=True, index=True,max_length=255)
  

class UserInDB(SQLModel):
    data:list[UserPublic]
    count:int
    
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

class Message(SQLModel):
    message: str


#items  
class ItemBase(SQLModel):
    title: str = Field (max_length=255,min_length=1)
    description: str | None = Field(default=None, max_length=225)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255, min_length=1)

class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False,ondelete="CASCADE")
    created_at: datetime | None = Field(default_factory=get_datetime_utc,sa_type=DateTime(timezone=True))
    owner: User |None = Relationship(back_populates="items")


class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None

class ItemsPublic(SQLModel):
    data:list[ItemPublic]
    count:int