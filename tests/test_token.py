import pytest
from datetime import timedelta
from app.config.security import create_access_token
from app.config.config import settings

def test_create_access_token():
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data, expires_delta)

    assert token is not None
    assert isinstance(token, str)