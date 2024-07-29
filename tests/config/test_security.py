from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi import HTTPException
from freezegun import freeze_time

from app.config.config import settings
from app.config.security import create_access_token
from app.users.application.use_cases import UserUseCase
from app.users.domain.repository_interface import UserRepositoryInterface


def test_create_access_token():
    data = {"sub": "user@example.com"}
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data, expires_delta)

    assert token is not None
    assert isinstance(token, str)


def test_create_access_token_invalid_data():
    with pytest.raises(ValueError):
        create_access_token(
            None, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )


def test_expiration_time(mocker):
    # Configuración del mock para settings
    mocker.patch.object(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    mocker.patch.object(settings, "SECRET_KEY", "test_secret")
    mocker.patch.object(settings, "ALGORITHM", "HS256")

    # Congelar el tiempo en un punto específico
    with freeze_time("2023-07-01 12:00:00") as frozen_time:
        data = {"sub": "user@example.com"}
        token = create_access_token(data)

        # Congelar el tiempo en el mismo punto para la verificación
        frozen_time.move_to("2023-07-01 12:00:00")
        TIME_EXP = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        tolerance = 5  # Tolerancia en segundos
        assert abs(decoded_token["exp"] - int(TIME_EXP.timestamp())) <= tolerance


# Invalid token raises an appropriate exception
def test_invalid_token_raises_exception(mocker):

    mock_user_repo = mocker.Mock(spec=UserRepositoryInterface)
    mock_user_repo.get_current_user.side_effect = HTTPException(
        status_code=401, detail="Invalid token"
    )

    user_use_case = UserUseCase(user_repository=mock_user_repo)
    token = "invalid_token"

    with pytest.raises(HTTPException) as exc_info:
        user_use_case.get_current_user(token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"


# Token for a non-existent user raises an appropriate exception
def test_non_existent_user_token_raises_exception(mocker):

    mock_user_repo = mocker.Mock(spec=UserRepositoryInterface)
    mock_user_repo.get_current_user.side_effect = HTTPException(
        status_code=404, detail="User not found"
    )

    user_use_case = UserUseCase(user_repository=mock_user_repo)
    token = "non_existent_user_token"

    with pytest.raises(HTTPException) as exc_info:
        user_use_case.get_current_user(token)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"
