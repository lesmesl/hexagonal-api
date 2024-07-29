import pytest
from sqlalchemy.orm import Session

from app.config.exceptions import DatabaseException
from app.users.infrastructure.repository import UserRepository


def test_empty_username(mocker):
    """
    Prueba para verificar que el método get_by_username devuelve None cuando se proporciona un nombre de usuario vacío.
    """

    mock_db = mocker.Mock(spec=Session)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    username = ""
    repo = UserRepository(mock_db)

    try:
        result = repo.get_by_username(username)
        assert result is None
    except DatabaseException:
        pytest.fail("DatabaseException was raised")
