
from fastapi.testclient import TestClient
from app.core.config import settings

def test_get_access_token(client: TestClient) -> None:

    response = client.post(
        f"{settings.API_V1_STR}/login/access-token",
        data={"username": settings.FIRST_SUPERUSER, "password": settings.EMAIL_TEST_USER_PASSWORD},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()