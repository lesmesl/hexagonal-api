from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

from app.config.config import settings
from app.config.database import get_db
from app.config.security import OAuth2PasswordRequestFormCustom, oauth2_scheme
from app.users.application.use_cases import UserUseCase
from app.users.infrastructure.dtos import (
    TokenResponseSchema,
    UserCreateSchema,
    UserResponseSchema,
)
from app.users.infrastructure.repository import UserRepository

router = APIRouter(tags=["Users"])


@router.post(
    settings.REGISTER_ROUTE,
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="Permite crear un nuevo usuario en la base de datos. Retorna la información del usuario sin la contraseña.",
)
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    use_cases = UserUseCase(user_repository)
    new_user = use_cases.create_user(user)
    return new_user


@router.post(
    settings.LOGIN_ROUTE,
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión",
    description="Permite iniciar sesión en la aplicación. Retorna el token de acceso.",
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestFormCustom = Depends(),
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    use_cases = UserUseCase(user_repository)
    return use_cases.login_user(form_data)


@router.get(
    settings.USERS_ME_ROUTE,
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Obtener información del usuario actual",
    description="Permite obtener la información del usuario autenticado en la aplicación.",
)
def read_users_me(db: Session = Depends(get_db), token: str = Security(oauth2_scheme)):
    user_repository = UserRepository(db)
    use_cases = UserUseCase(user_repository)
    current_user = use_cases.get_current_user(token)
    return current_user
