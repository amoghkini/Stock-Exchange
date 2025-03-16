from fastapi import APIRouter, status


router = APIRouter(prefix="/api/v1")


@router.get("/health", status_code=status.HTTP_200_OK)
async def check_server_health():
    return {"status": "ok"}