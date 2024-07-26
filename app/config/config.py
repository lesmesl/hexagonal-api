import os
from dotenv import load_dotenv
from app.config import constants as const

load_dotenv()


class Settings:
    PROJECT_NAME: str = const.PROJECT_NAME
    PROJECT_VERSION: str = const.PROJECT_VERSION
    API_V1_URL: str = const.API_V1_URL
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DEBUG: bool = True


settings = Settings
