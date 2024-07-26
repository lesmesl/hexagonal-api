from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", tags=["Users"])
async def test_users():
    return {"message": "Users pong"}
