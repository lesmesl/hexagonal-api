import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.config.database import get_db, Base
from app.config.config import settings

# Configuración de la base de datos para pruebas
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Fixture para la base de datos de pruebas
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
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
    yield TestClient(app)
    app.dependency_overrides[get_db] = get_db

# Fixture para crear un usuario de prueba
@pytest.fixture
def create_test_user(client_with_db):
    def _create_test_user(email: str, username: str, password: str):
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
    return _create_test_user
