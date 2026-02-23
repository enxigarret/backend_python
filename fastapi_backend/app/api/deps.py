
from sqlmodel import Session
from typing import Annotated
from collections.abc import Generator

from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]