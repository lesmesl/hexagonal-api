from fastapi import Request, status
from fastapi.responses import JSONResponse

from .exceptions import (
    DatabaseException,
    InvalidCredentialsException,
    InvalidTokenException,
    UserAlreadyExistsException,
)

def user_already_exists_exception_handler(
    request: Request, exc: UserAlreadyExistsException
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message},
    )


def invalid_credentials_exception_handler(
    request: Request, exc: InvalidCredentialsException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )


def invalid_token_exception_handler(request: Request, exc: InvalidTokenException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )


def database_exception_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )
