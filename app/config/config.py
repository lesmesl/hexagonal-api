import os

from dotenv import load_dotenv

from app.config import constants as const

load_dotenv()


class Settings:
    PROJECT_NAME: str = const.PROJECT_NAME
    PROJECT_VERSION: str = const.PROJECT_VERSION
    API_V1_URL: str = const.API_V1_URL
    REGISTER_ROUTE: str = const.REGISTER_ROUTE
    LOGIN_ROUTE: str = const.LOGIN_ROUTE
    USERS_ME_ROUTE: str = const.USERS_ME_ROUTE
    REGISTER_PRODUCTS_ROUTE: str = const.REGISTER_PRODUCTS_ROUTE
    GET_PRODUCTS_ROUTE: str = const.GET_PRODUCTS_ROUTE
    UPDATE_PRODUCTS_ROUTE: str = const.UPDATE_PRODUCTS_ROUTE
    DELETE_PRODUCTS_ROUTE: str = const.DELETE_PRODUCTS_ROUTE
    DESCRIPTION_PROJECT: str = const.DESCRIPTION_PROJECT
    TOKEN_URL: str = f"{API_V1_URL}{LOGIN_ROUTE}"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DEBUG: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    TEST_DATABASE_URL: str = const.TEST_DATABASE_URL


settings = Settings
