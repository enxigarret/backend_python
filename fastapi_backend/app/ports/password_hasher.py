from __future__ import annotations

from typing import Protocol


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str:
        ...

    def verify_and_update(
        self, plain_password: str, hashed_password: str
    ) -> tuple[bool, str | None]:
        ...

