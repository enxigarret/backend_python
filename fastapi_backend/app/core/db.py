from sqlmodel import SQLModel, create_engine,select, Session

from app.core.config import settings
from app import crud
from app.models import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)    

#.first() means: “give me the first row from this query result, or None if there are no rows.”
def init_db(session:Session) -> None:
    user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)).first()

    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud.user.create(session=session, obj_in=user_in)