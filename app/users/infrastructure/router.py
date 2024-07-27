from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.users.infrastructure.dtos import UserCreateSchema, UserResponseSchema
from app.users.infrastructure.repository import UserRepository
from app.users.application.register_user import RegisterUser
from app.config.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponseSchema)
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    register_user_case = RegisterUser(user_repository)
    try:
        new_user = register_user_case.execute(user)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/ping", tags=["Users"])
async def test_users():
    return {"message": "Users pong"}
