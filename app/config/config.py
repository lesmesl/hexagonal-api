import os

from dotenv import load_dotenv

from app.config import constants as const

load_dotenv()


class Settings:
    PROJECT_NAME: str = const.PROJECT_NAME
    PROJECT_VERSION: str = const.PROJECT_VERSION
    API_V1_URL: str = const.API_V1_URL

    LOGIN_ROUTE: str = const.LOGIN_ROUTE
    USERS_ME_ROUTE: str = const.USERS_ME_ROUTE
    TOKEN_URL: str = f"{API_V1_URL}/{LOGIN_ROUTE}"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DEBUG: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")


settings = Settings
