from __future__ import annotations

from app.core.security import get_password_hash, verify_password


class PwdlibPasswordHasher:
    def hash(self, password: str) -> str:
        return get_password_hash(password)

    def verify_and_update(
        self, plain_password: str, hashed_password: str
    ) -> tuple[bool, str | None]:
        return verify_password(plain_password, hashed_password)

