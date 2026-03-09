from fastapi.testclient import TestClient
from sqlmodel import Session
from app import crud
from app.core.config import settings
from app.models import UserCreate, UserUpdate

def user_authentication_header(
    *,
    client: TestClient,
    email: str,
    password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}
    response = client.post("/api/v1/login/access-token", data=data)
    token = response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

def authentication_token_from_email(
    *,
    client: TestClient,
    password: str = settings.EMAIL_TEST_USER_PASSWORD,
    email: str,
    db: Session
)->dict[str, str]:
    user = crud.get_user_by_email(session=db, email=email)
    if not user:
        user_in = UserCreate(email=email,password=password)
        user = crud.create_user(session=db, user_create=user_in)
    else:
        user_in_update=UserUpdate(email=email,password=password)
        if not user.id:
            raise Exception("User id not set")
        user = crud.update_user(session=db, db_user=user, user_in=user_in_update)
    return user_authentication_header(client=client, email=email, password=password)