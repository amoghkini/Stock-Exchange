from fastapi import APIRouter

from api.home.routes import router as home_router
from api.orders.routes import router as orders_router


api_router = APIRouter()

api_router.include_router(home_router, tags=["home"])
api_router.include_router(orders_router, tags=["orders"])
