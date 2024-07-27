from pydantic import BaseModel, EmailStr
from app.users.domain.model import User

class UserCreateSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        from_attributes = True
