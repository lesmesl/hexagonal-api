import uuid
from app.config.config import settings

def test_login_success(client_with_db, create_test_user):
    email = f"testuser{uuid.uuid4()}@example.com"
    username = f"testuser{uuid.uuid4()}"
    password = "testpassword"
    
    # Registrar el usuario de prueba
    create_test_user(email, username, password)

    # Intentar iniciar sesión con el usuario de prueba
    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.LOGIN_ROUTE}",
        data={
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "",
            "client_id": "",
            "client_secret": ""
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_failure(client_with_db):
    # Intentar iniciar sesión con credenciales incorrectas
    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.LOGIN_ROUTE}",
        data={
            "grant_type": "password",
            "username": "wronguser",
            "password": "wrongpassword",
            "scope": "",
            "client_id": "",
            "client_secret": ""
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}
