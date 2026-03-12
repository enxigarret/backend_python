
from fastapi.testclient import TestClient
from app.core.config import settings
from app.main import app
from unittest.mock import patch


def test_get_access_token(client: TestClient) -> None:
    for route in app.routes:
        print(route.path)

    response = client.post(
        f"{settings.API_V1_STR}/auth/login/access-token",
        data={"username": settings.EMAIL_TEST_USER, "password": settings.EMAIL_TEST_USER_PASSWORD},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_recovery_password(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    with (
        patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
        patch("app.core.config.settings.SMTP_USER", "admin@example.com"),
    ):
        email = "test@example.com"
        r = client.post(
            f"{settings.API_V1_STR}/auth/password-recovery/{email}",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 200
        # assert r.json() == {
        #     "message": "If that email is registered, we sent a password recovery link"
        # }
