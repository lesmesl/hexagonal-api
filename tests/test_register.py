import uuid
from app.config.config import settings

def test_register_success(client_with_db):
    email = f"testuser{uuid.uuid4()}@example.com"
    username = f"testuser{uuid.uuid4()}"
    password = "testpassword"

    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.REGISTER_ROUTE}",
        json={
            "email": email,
            "username": username,
            "password": password
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    assert response.status_code == 200
