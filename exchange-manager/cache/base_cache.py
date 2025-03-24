import logging
from abc import ABC, abstractmethod
from typing import Literal

from cache.cache import Cache


class BaseCache:
    
    def __init__(
        self,
        cache_type: Literal[Cache.REDIS, Cache.MEMORY]
    ) -> None:
        self.cache_type = cache_type
        logging.info(f"The cache is initialized with {cache_type} type")
    
    @abstractmethod    
    async def get(self, key):
        raise NotImplementedError
    
    @abstractmethod
    async def set(self, key, value):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key):
        raise NotImplementedError
    
    @abstractmethod
    async def clear(self):
        raise NotImplementedError