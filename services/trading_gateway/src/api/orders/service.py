import logging
import os

from api.orders.schemas import Order
from cache.redis_manager import RedisManager

class OrderService:
    
    async def place_order(
        self,
        order_data: Order
    ) -> dict:
        logging.info('Going to place an order')
        
        # add order to queue
        redis = RedisManager.get_instance()
        if os.getenv("wait_for_fills", "True") == "True":
            response = await redis.send_order_and_await_for_fills(order_data.to_dict())
        else:
            response = await redis.send_order_to_queue(order_data.to_dict())
        
        return response