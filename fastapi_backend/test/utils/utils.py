
from fastapi.testclient import TestClient
from app.core.config import settings


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {"username": settings.FIRST_SUPERUSER, "password": settings.FIRST_SUPERUSER_PASSWORD}

    response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    token = response.json().get("access_token")
    #return auth headers with the token
    return {"Authorization": f"Bearer {token}"}

