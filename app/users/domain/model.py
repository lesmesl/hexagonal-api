from dataclasses import dataclass

from pydantic import EmailStr


@dataclass
class User:
    username: str
    email: EmailStr
    password: str
