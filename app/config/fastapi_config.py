from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import settings
from app.config.error_handlers import (
    generic_exception_handler,
    invalid_credentials_exception_handler,
    user_already_exists_exception_handler,
)
from app.config.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
)
from app.products.infrastructure.router import router as products_router
from app.users.infrastructure.router import router as users_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API following Hexagonal Architecture principles",
        version=settings.PROJECT_VERSION,
        redoc_url=None,
        docs_url="/docs",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_v1 = APIRouter(prefix=settings.API_V1_URL)
    api_v1.include_router(products_router, prefix="/products", tags=["Products"])
    api_v1.include_router(users_router, tags=["Users"])
    app.include_router(api_v1)

    app.add_exception_handler(
        UserAlreadyExistsException, user_already_exists_exception_handler
    )
    app.add_exception_handler(
        InvalidCredentialsException, invalid_credentials_exception_handler
    )
    app.add_exception_handler(Exception, generic_exception_handler)

    return app
