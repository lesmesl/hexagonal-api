from app.config.config import settings


def test_register_user_success(client_with_db, data_login_user):
    """
    Prueba que un usuario se registre con éxito.
    """
    email, username, password = data_login_user

    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.REGISTER_ROUTE}",
        json={"email": email, "username": username, "password": password},
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    assert response.status_code == 201


def test_login_user_success(client_with_db, create_test_user, data_login_user):
    """
    Prueba que un usuario inicie sesión con éxito.
    """
    email, username, password = data_login_user

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


def test_login_user_failure(client_with_db):
    """
    Prueba que el inicio de sesión falle con credenciales incorrectas.
    """
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


def test_register_user_already_registered(
    client_with_db, data_login_user, create_test_user
):
    """
    Prueba que no se pueda registrar un usuario con un email o username ya registrado.
    """
    email, username, password = data_login_user

    # Registrar el usuario de prueba
    create_test_user(email, username, password)

    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.REGISTER_ROUTE}",
        json={"email": email, "username": username, "password": password},
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Email or Username already registered"}


def test_get_current_user_success(client_with_db, create_test_user, data_login_user):
    """
    Prueba que se obtenga la información del usuario autenticado con éxito.
    """
    email, username, password = data_login_user

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


def test_get_current_user_no_token(client_with_db):
    """
    Prueba que obtener la información del usuario falle sin token de autenticación.
    """
    response = client_with_db.get(
        f"{settings.API_V1_URL}{settings.USERS_ME_ROUTE}",
        headers={"accept": "application/json"},
    )

    # Verificar que la respuesta sea un error 401 (Unauthorized)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
