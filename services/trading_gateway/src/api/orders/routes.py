from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api.orders.schemas import OrderCreateModel


router = APIRouter(prefix="/api/v1/orders")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreateModel
) -> JSONResponse:
    print(order_data)
    return JSONResponse(
        content={
            "message": "Order placed successully"
        }
    )