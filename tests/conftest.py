# tests/conftest.py
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
