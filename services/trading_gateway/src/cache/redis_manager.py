import logging
import os
from typing import Any, Optional

from exchange_manager.cache.redis_cache import AsyncRedisCache


class RedisManager:
    
    __instance: Optional["RedisManager"] = None
    
    def __init__(self) -> None:
        if RedisManager.__instance:
            raise Exception("This is a singleton class. Please use get_instance funtion to reuse the existing instance.")    
        else:
            logging.info("Going to create instance for the first time")
            RedisManager.__instance = self
            logging.info("Instance created for the first time.")
    
    
        # create redis instance
        self.redis = AsyncRedisCache(
            host=os.getenv("QUEUE_REDIS_HOST", "exchange_redis"),
            port=int(os.getenv("QUEUE_REDIS_PORT", 6379)),
            db=0
        )
        
    @classmethod
    def get_instance(cls) -> "RedisManager":
        if not cls.__instance:
            logging.info("Creating new redisinstance")
            cls()
        return cls.__instance
    
    async def send_order(self, data: Any) -> None:
        logging.info("Going to add order to queue")
        await self.redis.enqueue("orders", data)
        logging.info("Order added to queue")
    
    async def send_order_and_await_for_fills(self):
        # TODO: implement this
        pass
    
if __name__ == "__main__":
    RedisManager.get_instance()
    logging.info("1st call completed successfully")
    RedisManager.get_instance()