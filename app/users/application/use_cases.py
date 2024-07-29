from datetime import timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.config.config import settings
from app.config.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
)
from app.config.security import create_access_token, get_password_hash, verify_password
from app.users.domain.repository_interface import UserRepositoryInterface
from app.users.infrastructure.dtos import (
    TokenResponseSchema,
    UserCreateSchema,
    UserResponseSchema,
)


class UserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def create_user(self, user_data: UserCreateSchema) -> UserResponseSchema:
        if self.user_repository.validate_by_email_username(
            user_data.email, user_data.username
        ):
            raise UserAlreadyExistsException()

        hashed_password = get_password_hash(user_data.password)
        user_data.password = hashed_password

        # patrón builder para convertir UserCreateSchema a User antes de llamar al método create de la interfaz UserRepositoryInterface.
        user_data.to_user()
        new_user = self.user_repository.create(user_data)

        return UserResponseSchema.model_validate(new_user)

    def login_user(
        self, form_data: OAuth2PasswordRequestForm = Depends()
    ) -> TokenResponseSchema:
        user = self.user_repository.get_by_username(form_data.username)
        if not user or not verify_password(form_data.password, user.password):
            raise InvalidCredentialsException()

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        token_data = {"access_token": access_token, "token_type": "bearer"}
        return TokenResponseSchema.model_validate(token_data)

    def get_current_user(self, token: str) -> UserResponseSchema:
        user = self.user_repository.get_current_user(token)
        return UserResponseSchema.model_validate(user)
