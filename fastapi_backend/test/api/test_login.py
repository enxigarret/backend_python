
from fastapi.testclient import TestClient
from app.core.config import settings
from app.main import app


def test_get_access_token(client: TestClient) -> None:
    for route in app.routes:
        print(route.path)

    response = client.post(
        f"{settings.API_V1_STR}/auth/login/access-token",
        data={"username": settings.EMAIL_TEST_USER, "password": settings.EMAIL_TEST_USER_PASSWORD},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()