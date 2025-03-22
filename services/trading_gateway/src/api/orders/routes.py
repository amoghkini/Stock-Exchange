from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api.orders.schemas import OrderCreateModel


router = APIRouter(prefix="/api/v1/orders")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreateModel
) -> JSONResponse:
    print(order_data)
    add_to_queue(order_data)
    return JSONResponse(
        content={
            "message": "Order placed successully"
        }
    )
    
def add_to_queue(order_data):
    import redis
    import os

    queue = redis.Redis(
        host=os.getenv("QUEUE_REDIS_HOST", "exchange_redis"),
        port=int(os.getenv("QUEUE_REDIS_PORT", 6379)),
        db=0
    )
    order_data_json = order_data.json()
    print("Adding order to queue:", order_data_json)
    queue.lpush("orders_queue", order_data_json)
    print("Order added to queue")