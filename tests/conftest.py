# tests/conftest.py
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.config import settings
from app.config.database import Base, get_db
from app.main import app

# Configuración de la base de datos para pruebas
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Fixture para la base de datos de pruebas
@pytest.fixture(scope="function")
def db():
    from app.users.infrastructure.models import UserDTO  # noqa

    # Crear todas las tablas
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Eliminar todas las tablas después de la prueba
        Base.metadata.drop_all(bind=test_engine)


# Fixture para el cliente de pruebas con la base de datos de pruebas
@pytest.fixture(scope="function")
def client_with_db(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# Fixture para crear un usuario de prueba
@pytest.fixture
def create_test_user(client_with_db):
    def _create_test_user(email: str, username: str, password: str):
        response = client_with_db.post(
            f"{settings.API_V1_URL}{settings.REGISTER_ROUTE}",
            json={"email": email, "username": username, "password": password},
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        assert response.status_code == 200

    return _create_test_user


@pytest.fixture
def data_login_user():
    email = f"testuser{uuid.uuid4()}@example.com"
    username = f"testuser{uuid.uuid4()}"
    password = "testpassword"
    return email, username, password


@pytest.fixture
def data_product_success():
    return {
        "name": "Test Product",
        "price": 10.2,
        "in_stock": True,
        "description": "description",
    }


@pytest.fixture
def test_login_token(client_with_db, create_test_user, data_login_user):

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

    response_json = response.json()
    return response_json.get("access_token")


@pytest.fixture
def test_create_product_success(client_with_db, test_login_token, data_product_success):

    token = test_login_token

    response = client_with_db.post(
        f"{settings.API_V1_URL}{settings.REGISTER_PRODUCTS_ROUTE}",
        json=data_product_success,
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201
