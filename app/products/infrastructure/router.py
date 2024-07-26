from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", tags=["Products"])
async def test_products():
    return {"message": "Products pong"}
