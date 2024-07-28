import uuid

from app.config.config import settings


def test_register_success(client_with_db):
    email = f"testuser{uuid.uuid4()}@example.com"
    username = f"testuser{uuid.uuid4()}"
    password = "testpassword"

    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.REGISTER_ROUTE}",
        json={"email": email, "username": username, "password": password},
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    assert response.status_code == 200


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
            "client_secret": "",
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_failure(client_with_db):
    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.LOGIN_ROUTE}",
        data={
            "grant_type": "password",
            "username": "wronguser",
            "password": "wrongpassword",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_read_users_me(client_with_db, create_test_user):
    email = f"testuser{uuid.uuid4()}@example.com"
    username = f"testuser{uuid.uuid4()}"
    password = "testpassword"

    # Registrar el usuario de prueba
    create_test_user(email, username, password)

    # Iniciar sesión con el usuario de prueba para obtener el token de acceso
    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.LOGIN_ROUTE}",
        data={
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert response.status_code == 200
    response_json = response.json()
    access_token = response_json.get("access_token")

    assert access_token is not None

    # Usar el token de acceso para obtener la información del usuario actual
    response = client_with_db.get(
        f"{settings.API_V1_URL}{settings.USERS_ME_ROUTE}",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200


def test_users_ping_no_auth(client_with_db):
    response = client_with_db.get(f"{settings.API_V1_URL}/ping")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_read_users_me_no_token(client_with_db):
    response = client_with_db.get(
        f"{settings.API_V1_URL}{settings.USERS_ME_ROUTE}",
        headers={"accept": "application/json"},
    )

    # Verificar que la respuesta sea un error 401 (Unauthorized)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
