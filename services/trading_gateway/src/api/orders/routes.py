import stat
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api.orders.schemas import Order
from api.orders.service import OrderService


router = APIRouter(prefix="/api/v1/orders")
service = OrderService()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: Order
) -> JSONResponse:
    response = await service.place_order(order_data)
    return JSONResponse(
        content=response,
        status_code=status.HTTP_201_CREATED,
        media_type="application/json",
    )
