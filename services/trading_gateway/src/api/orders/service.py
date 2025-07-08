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
        message = {
            "type": "CREATE_ORDER", 
            "data": order_data.to_dict()
        }
        
        if os.getenv("wait_for_fills", "False") == "True":
            response = await redis.send_order_and_await_for_fills(message)
        else:
            response = await redis.send_order_to_queue(message)
        
        return response