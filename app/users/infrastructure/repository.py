from sqlalchemy.orm import Session
from app.users.domain.model import User
from app.users.infrastructure.models import UserDTO
from app.users.infrastructure.dtos import UserCreateSchema, UserResponseSchema
from sqlalchemy import or_
from typing import Optional
from app.config.database import get_db
from fastapi import Depends


class UserRepository():
    def __init__(self, db: Session):
        self.db = db

    def validate_by_email_username(self, email: str, username: str) -> bool:
        user = self.db.query(UserDTO).filter(or_(UserDTO.email == email, UserDTO.username == username)).first()
        return user is not None

    def create(self, user_data: UserCreateSchema) -> UserResponseSchema:
        new_user = UserDTO(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(UserDTO).filter(UserDTO.email == email).first()