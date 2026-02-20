from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from pwdlib.hashers.argon2 import Argon2Hasher

import jwt
from datetime import datetime, timedelta, timezone
from typing import Any
from app.core.config import settings

password_hash = PasswordHash(
    [
        BcryptHasher(),
        Argon2Hasher(),
    ]
)

ALGORITHM = "HS256"

#expires_delta is a timedelta object that specifies how long the token should be valid for
def create_access_token(subject: str | Any,expires_delta:timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(
    plain_password: str, hashed_password: str
) -> tuple[bool, str | None]:
    return password_hash.verify_and_update(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

