from fastapi import APIRouter, status


home_router = APIRouter()


@home_router.get('/health', status_code=status.HTTP_200_OK)
async def check_server_health():
    return {"status": "ok"}