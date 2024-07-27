from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config.config import settings
from app.users.domain.model import User
from app.users.infrastructure.dtos import UserCreateSchema, UserResponseSchema
from app.users.infrastructure.models import UserDTO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_URL}/users/token")


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def validate_by_email_username(self, email: str, username: str) -> bool:
        user = (
            self.db.query(UserDTO)
            .filter(or_(UserDTO.email == email, UserDTO.username == username))
            .first()
        )
        return user is not None

    def create(self, user_data: UserCreateSchema) -> UserResponseSchema:
        new_user = UserDTO(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(UserDTO).filter(UserDTO.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(UserDTO).filter(UserDTO.username == username).first()

    def get_current_user(
        self, token: str = Depends(oauth2_scheme)
    ) -> UserResponseSchema:
        credentials_exception = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = self.get_by_email(payload.get("sub"))

        if user is None:
            raise credentials_exception
        return user
