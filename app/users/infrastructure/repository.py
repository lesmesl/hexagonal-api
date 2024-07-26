from sqlalchemy.orm import Session
from app.users.domain.repository_interface import UserRepositoryInterface
from app.users.domain.model_schemas import UserCreateSchema, UserResponseSchema
from app.users.infrastructure.models import User
from sqlalchemy import or_

class UserRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def validate_by_email_username(self, email: str, username: str) -> bool:
        user = self.db.query(User).filter(or_(User.email == email, User.username == username)).first()
        return user is not None

    def create(self, user_data: UserCreateSchema) -> UserResponseSchema:
        new_user = User(**user_data.dict())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user