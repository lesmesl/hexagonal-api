from typing import Optional

from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.config.config import settings
from app.config.database import get_db
from app.config.exceptions import DatabaseException, InvalidTokenException
from app.users.domain.model import User
from app.users.domain.repository_interface import UserRepositoryInterface
from app.users.infrastructure.dtos import UserCreateSchema, UserResponseSchema
from app.users.infrastructure.models import UserDTO


class UserRepository(UserRepositoryInterface):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def validate_by_email_username(self, email: str, username: str) -> bool:
        try:
            user = (
                self.db.query(UserDTO)
                .filter(or_(UserDTO.email == email, UserDTO.username == username))
                .first()
            )
            return user is not None
        except Exception as e:
            raise DatabaseException(
                f"Error validating user by email or username. detail: {str(e)}"
            )

    def create(self, user_data: UserCreateSchema) -> UserResponseSchema:
        try:
            new_user = UserDTO(
                email=user_data.email,
                username=user_data.username,
                password=user_data.password,
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except Exception as e:
            self.db.rollback()
            raise DatabaseException(f"Error creating user. detail: {str(e)}")

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            return self.db.query(UserDTO).filter(UserDTO.email == email).first()
        except Exception as e:
            raise DatabaseException(f"Error getting user by email. detail: {str(e)}")

    def get_by_username(self, username: str) -> Optional[User]:
        try:
            return self.db.query(UserDTO).filter(UserDTO.username == username).first()
        except Exception as e:
            raise DatabaseException(f"Error getting user by username. detail: {str(e)}")

    def get_current_user(self, token: str) -> UserResponseSchema:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise InvalidTokenException
        except JWTError:
            raise InvalidTokenException

        user = self.get_by_email(payload.get("sub"))

        if user is None:
            raise InvalidTokenException
        return user
