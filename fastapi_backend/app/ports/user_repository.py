from __future__ import annotations

import uuid
from typing import Protocol

from app.models import User


class UserRepository(Protocol):
    def add(self, user: User) -> User:
        ...

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        ...

    def get_by_email(self, email: str) -> User | None:
        ...

