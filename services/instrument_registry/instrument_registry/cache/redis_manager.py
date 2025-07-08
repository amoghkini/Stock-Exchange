import json
import os
import logging
from typing import Optional

from exchange_manager.cache.redis_cache import AsyncRedisCache
from exchange_manager.core.exceptions import SingletonClassException
from exchange_manager.utils.time_utils import TimeUtils


class RedisManager:
    """
    This class provides methods for interacting with the Redis cache.
    """
    
    __instance: Optional["RedisManager"] = None

    def __init__(self) -> None:
        if RedisManager.__instance:
            raise SingletonClassException(
                "RedisManager is a singleton class. Please use get_instance funtion to reuse the existing instance."
            )
        else:
            logging.info("Going to create instance for the first time")
            RedisManager.__instance = self
            logging.info("Instance created for the first time.")

        # create redis instance
        self.redis = AsyncRedisCache(
            host=os.getenv("QUEUE_REDIS_HOST", "139.59.18.104"),
            port=int(os.getenv("QUEUE_REDIS_PORT", "6379")),
            db=0,
        )

    @classmethod
    def get_instance(cls) -> "RedisManager":
        """Get the singleton instance of the RedisManager class."""
        if not cls.__instance:
            cls()
        return cls.__instance  # type: ignore

    @classmethod
    def get_instrument_key_for_date(
        cls, 
        date: str
    ) -> str:
        """Get the key for the instruments cache by date."""
        return f"instruments:{date}"
    
    async def get_cached_instruments(
        self,
        trade_date: Optional[str] = None,
    ) -> Optional[dict[str, dict[str, str]]]:
        """Get the instruments from the cache by date."""
        if not trade_date:
            trade_date = TimeUtils.get_todays_date_str()

        instrument_key: str = RedisManager.get_instrument_key_for_date(trade_date)
        data = await self.redis.get(instrument_key)
        return json.loads(data) if data else None

    async def set_cached_instruments(
        self,
        trade_date: str,
        data: dict[str, dict[str, str]],
        expire: int = 60 * 60 * 24 * 7,
    ) -> None:
        """Set the instruments in the cache by date."""
        instrument_key: str = RedisManager.get_instrument_key_for_date(trade_date)
        await self.redis.set(instrument_key, json.dumps(data), expire=expire)

    async def delete_cached_instruments(
        self,
        trade_date: str,
    ) -> None:
        """Delete the instruments from the cache by date."""
        instrument_key: str = RedisManager.get_instrument_key_for_date(trade_date)
        await self.redis.delete(instrument_key)
