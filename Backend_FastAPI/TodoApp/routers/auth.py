from fastapi import APIRouter
from litellm import router

router = APIRouter()

@router.get("/auth/")
async def get_user() -> dict[str, str]:
    return {'user': 'authenticate'}