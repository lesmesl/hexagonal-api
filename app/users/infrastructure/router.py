from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.users.infrastructure.dtos import UserCreateSchema, UserResponseSchema, UserLoginSchema
from app.users.infrastructure.repository import UserRepository
from app.users.application.use_cases import UserUseCase
from app.config.database import get_db

router = APIRouter()
user_repository = UserRepository(get_db())
use_cases = UserUseCase(user_repository)


@router.post("/register", response_model=UserResponseSchema)
def register_user(user: UserCreateSchema):
    try:
        new_user = use_cases.create_user(user)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login_user(user: UserLoginSchema):
    try:
        token = use_cases.login_user(user)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/ping", tags=["Users"])
async def test_users():
    return {"message": "Users pong"}
