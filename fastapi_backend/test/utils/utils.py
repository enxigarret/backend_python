
from fastapi.testclient import TestClient
from app.core.config import settings

def get_sueruser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {"username": settings.first_superuser_email, "password": settings.first_superuser_password}

    response = client.post("/api/v1/login/access-token", data=login_data)
    token = response.json().get("access_token")
    #return auth headers with the token
    return {"Authorization": f"Bearer {token}"}