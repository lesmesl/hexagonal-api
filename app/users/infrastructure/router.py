from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.config.database import get_db
from app.users.application.use_cases import UserUseCase, oauth2_scheme
from app.users.infrastructure.dtos import Token, UserCreateSchema, UserResponseSchema
from app.users.infrastructure.repository import UserRepository
from app.config.config import settings

router = APIRouter()
user_repository = UserRepository(get_db())
use_cases = UserUseCase(user_repository)


@router.post(settings.REGISTER_ROUTE, response_model=UserResponseSchema)
def register_user(user: UserCreateSchema):
    try:
        new_user = use_cases.create_user(user)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(settings.LOGIN_ROUTE, response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        token = use_cases.login_user(form_data)
        return token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(settings.USERS_ME_ROUTE, response_model=UserResponseSchema)
def read_users_me(token: str = Depends(oauth2_scheme)):
    current_user = use_cases.get_current_user(token)
    return current_user


@router.get(settings.PING_ROUTE)
def ping(current_user: str = Depends(oauth2_scheme)):
    return {"message": "pong"}
