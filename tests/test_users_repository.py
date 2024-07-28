import pytest

def test_empty_username(mocker):
    from app.users.infrastructure.repository import UserRepository
    from app.config.exceptions import DatabaseException
    from sqlalchemy.orm import Session

    # Mock the database session
    mock_db = mocker.Mock(spec=Session)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    username = "" 
    repo = UserRepository(mock_db)

    try:
        result = repo.get_by_username(username)
        assert result is None
    except DatabaseException:
        pytest.fail("DatabaseException was raised")