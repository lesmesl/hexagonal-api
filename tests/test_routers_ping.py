from fastapi.testclient import TestClient

from app.config.config import settings
from app.main import app

client = TestClient(app)


def test_products_no_ping():
    response = client.get(f"{settings.API_V1_URL}/products/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "Products pong"}

def test_users_ping_no_auth():
    response = client.get(f"{settings.API_V1_URL}/ping")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
