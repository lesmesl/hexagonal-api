from dataclasses import dataclass

@dataclass
class UserCreateSchema:
    email: str
    username: str
    password: str

@dataclass
class UserResponseSchema:
    id: int
    email: str
    username: str