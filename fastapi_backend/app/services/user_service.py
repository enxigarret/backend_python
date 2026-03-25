from __future__ import annotations

from typing import Any

from app.models import User, UserCreate, UserUpdate
from app.ports.password_hasher import PasswordHasher
from app.ports.user_repository import UserRepository

# Dummy hash to use for timing attack prevention when a user is not found.
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


class UserService:
    def __init__(
        self,
        *,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def create_user(self, user_create: UserCreate) -> User:
        user = User.model_validate(
            user_create,
            update={"hashed_password": self.password_hasher.hash(user_create.password)},
        )
        return self.user_repository.add(user)

    def update_user(self, db_user: User, user_update: UserUpdate) -> Any:
        user_data = user_update.model_dump(exclude_unset=True)
        extra_data: dict[str, str] = {}

        if "password" in user_data:
            extra_data["hashed_password"] = self.password_hasher.hash(
                user_data.pop("password")
            )

        db_user.sqlmodel_update(user_data, update=extra_data)
        return self.user_repository.add(db_user)

    def get_user_by_email(self, email: str) -> User | None:
        return self.user_repository.get_by_email(email)

    def authenticate(self, *, email: str, password: str) -> User | None:
        db_user = self.user_repository.get_by_email(email)
        if not db_user:
            self.password_hasher.verify_and_update(password, DUMMY_HASH)
            return None

        verified, updated_password_hash = self.password_hasher.verify_and_update(
            password, db_user.hashed_password
        )
        if not verified:
            return None

        if updated_password_hash:
            db_user.hashed_password = updated_password_hash
            db_user = self.user_repository.add(db_user)

        return db_user

