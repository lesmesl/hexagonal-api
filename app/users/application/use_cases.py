from app.users.domain.repository_interface import UserRepositoryInterface
from app.config.security import get_password_hash
from app.users.infrastructure.dtos import UserCreateSchema, UserResponseSchema, UserLoginSchema
from app.users.infrastructure.repository import UserRepository
from app.config.security import create_access_token, verify_password
from fastapi import HTTPException


class UserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def create_user(self, user_data: UserCreateSchema) -> UserResponseSchema:
        if self.user_repository.validate_by_email_username(user_data.email, user_data.username):
            raise ValueError("Email o Username already registered")
        
        hashed_password = get_password_hash(user_data.password)
        user_data.password = hashed_password
        
        # patrón builder para convertir UserCreateSchema a User antes de llamar al método create de la interfaz UserRepositoryInterface.
        user = user_data.to_user()
        new_user = self.user_repository.create(user_data)

        return UserResponseSchema.from_orm(new_user)
    
    def login_user(self, user_data: UserLoginSchema) -> str:
        user = self.user_repository.get_by_email(user_data.email)
        if not user or not verify_password(user_data.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        token = create_access_token(data={"sub": user.email})
        return token