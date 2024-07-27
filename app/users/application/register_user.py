from app.users.domain.repository_interface import UserRepositoryInterface
from app.config.security import get_password_hash
from app.users.infrastructure.dtos import UserCreateSchema, UserResponseSchema

class RegisterUser:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, user_data: UserCreateSchema) -> UserResponseSchema:
        if self.user_repository.validate_by_email_username(user_data.email, user_data.username):
            raise ValueError("Email o Username already registered")
        
        hashed_password = get_password_hash(user_data.password)
        user_data.password = hashed_password
        new_user = self.user_repository.create(user_data)
        return UserResponseSchema.from_orm(new_user)