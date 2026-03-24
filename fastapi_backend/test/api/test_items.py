



from urllib import response
from xmlrpc import client

from fastapi.testclient import TestClient


from app.core.config import settings


def test_create_item(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    data = {"title": "Test Item", "description": "This is a test item."}
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == "Test Item"
    assert content["description"] == "This is a test item."
    assert "id" in content
