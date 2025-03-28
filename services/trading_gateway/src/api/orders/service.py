import logging

from api.orders.schemas import OrderCreateModel
from cache.redis_manager import RedisManager

class OrderService:
    
    async def place_order(
        self,
        order_data: OrderCreateModel
    ) -> dict:
        logging.info('Going to place an order')
        
        # add order to queue
        redis = RedisManager.get_instance()
        await redis.send_order(order_data)
        
        return {
            "message": "Order placed successfully"
        }