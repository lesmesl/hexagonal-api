from pydantic import BaseModel, EmailStr
from app.users.domain.model import User

class UserCreateSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

    def to_user(self) -> User:
        return User(
            email=self.email,
            username=self.username,
            password=self.password,
        )

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        from_attributes = True
