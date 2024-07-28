from pydantic import BaseModel, ConfigDict, EmailStr

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

    model_config = ConfigDict(from_attributes=True)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)
