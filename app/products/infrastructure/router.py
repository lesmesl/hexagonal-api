from fastapi import APIRouter

from app.config.config import settings

router = APIRouter()


@router.get(settings.PING_ROUTE, tags=["Products"])
async def test_products():
    return {"message": "Products pong"}
