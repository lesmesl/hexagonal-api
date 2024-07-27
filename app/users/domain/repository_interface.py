from abc import ABC, abstractmethod
from app.users.domain.model import User
from typing import Optional


class UserRepositoryInterface(ABC):
    @abstractmethod
    def validate_by_email_username(self, email: str, username: str):
        pass

    @abstractmethod
    def create(self, user_data: User) -> User:
        pass