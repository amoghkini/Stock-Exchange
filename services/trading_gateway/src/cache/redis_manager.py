import logging
import os
from typing import Any, Optional

from exchange_manager.cache.redis_cache import AsyncRedisCache


class RedisManager:
    
    __instance: Optional["RedisManager"] = None
    
    def __init__(self) -> None:
        if RedisManager.__instance:
            raise Exception("RedisManager is a singleton class. Please use get_instance funtion to reuse the existing instance.")
        else:
            logging.info("Going to create instance for the first time")
            RedisManager.__instance = self
            logging.info("Instance created for the first time.")

        # create redis instance
        self.redis = AsyncRedisCache(
            host=os.getenv("QUEUE_REDIS_HOST", "exchange-redis"),
            port=int(os.getenv("QUEUE_REDIS_PORT", 6379)),
            db=0
        )
        
    @classmethod
    def get_instance(cls) -> "RedisManager":
        if not cls.__instance:
            cls()
        return cls.__instance
    
    async def send_order_to_queue(self, data: dict[str, Any]) -> dict[str, Any]:
        logging.info("Going to add order to queue")
        await self.redis.enqueue("orders", data)
        logging.info("Order added to queue")
        return {
            "message": "Order placed successfully"
        }
    
    async def one_shot_subscribe(self, channel: str) -> Any:
        pubsub = await self.redis.subscribe(channel)

        try:
            async for message in self.redis.listen(pubsub):
                await self.redis.unsubscribe(pubsub, channel)
                return message
        finally:
            await pubsub.close()
        
    async def send_order_and_await_for_fills(self, data: dict[str, Any]) -> dict[str, Any]:
        await self.send_order_to_queue(data)
        logging.info("Order added to queue. Waiting for fills...")
        # subscribe to a channel and wait for messages
        channel = f"order_fill:{data['order_id']}"

        fill_message = await self.one_shot_subscribe(channel)
        logging.info(f"Fill message received: {fill_message}")
        return {
        "message": "Order filled",
        "fill": fill_message
    }
        
if __name__ == "__main__":
    RedisManager.get_instance()
    logging.info("1st call completed successfully")
    RedisManager.get_instance()