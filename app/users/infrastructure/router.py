from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config.config import settings
from app.config.database import get_db
from app.users.application.use_cases import UserUseCase, oauth2_scheme
from app.users.infrastructure.dtos import (
    TokenResponseSchema,
    UserCreateSchema,
    UserResponseSchema,
)
from app.users.infrastructure.repository import UserRepository

router = APIRouter()


@router.post(settings.REGISTER_ROUTE, response_model=UserResponseSchema)
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    use_cases = UserUseCase(user_repository)
    new_user = use_cases.create_user(user)
    return new_user


@router.post(settings.LOGIN_ROUTE, response_model=TokenResponseSchema)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user_repository = UserRepository(db)
    use_cases = UserUseCase(user_repository)
    return use_cases.login_user(form_data)


@router.get(settings.USERS_ME_ROUTE, response_model=UserResponseSchema)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    use_cases = UserUseCase(user_repository)
    current_user = use_cases.get_current_user(token)
    return current_user


@router.get(settings.PING_ROUTE)
def ping(current_user: str = Depends(oauth2_scheme)):
    return {"message": "pong"}
