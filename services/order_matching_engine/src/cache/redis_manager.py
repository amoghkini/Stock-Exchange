import os
import logging
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
        return cls.__instance #type: ignore

    
    async def order_lister(self) -> Any:
        order_data = await self.redis.dequeue("orders", block=True)
        return order_data
    
    async def send_to_trading_gateway(self, channel: str, order: dict[str, Any]) -> None:
        await self.redis.publish(channel, order)