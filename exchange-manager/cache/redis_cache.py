import logging
import pickle
import asyncio
from typing import Optional, Any
from redis import asyncio as aioredis


class AsyncRedisCache:
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        password: Optional[str] = None
    ) -> None:
        logging.info("Initializing Redis cache")
        self.redis = self.__connect(host, port, db, password)
        
        logging.info("Redis cache initialized. Going to test the connection...")

        # sync call to test connection
        self.test_connection()

    def __connect(
        self,
        host: str,
        port: int,
        db: int,
        password: Optional[str] = None
    ) -> aioredis.Redis:
        return aioredis.Redis(
            host=host,
            port=port,
            db=db,
            password=password
        )

    async def async_test_connection(self) -> bool:
        """Asynchronously test the connection to the Redis server."""
        try:
            return await self.redis.ping()
        except Exception as e:
            logging.error(f"Redis connection test failed: {e}")
            return False

    def test_connection(self):
        """Synchronously test the connection to the Redis server."""
        try:
            return self.redis.ping() if self.redis else False
        except Exception:
            return False

    def __repr__(self):
        return f"<AsyncRedisCache host={self.redis.connection_pool.connection_kwargs['host']} port={self.redis.connection_pool.connection_kwargs['port']} db={self.redis.connection_pool.connection_kwargs['db']}>"

    def __str__(self):
        return self.__repr__()

    def __enter__(self):
        return self
    
    async def __aenter__(self):
        return self

    async def close(self):
        if self.redis:
            await self.redis.close()
            logging.info("Redis cache closed")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sync exit method."""
        asyncio.run(self.close())

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async exit method."""
        await self.close()

    def __del__(self):
        """Destructor to close the connection."""
        if self.redis:
            try:
                asyncio.run(self.close())
            except Exception as e:
                logging.error(f"Error closing Redis: {e}")

    async def set(
        self, 
        key: str, 
        value: Any, 
        expire: Optional[int] = None
    ) -> None:
        """Set a key-value pair in Redis asynchronously."""
        await self.redis.set(key, pickle.dumps(value), ex=expire)

    async def get(
        self, 
        key: str
    ) -> Optional[Any]:
        """Get the value of a key from Redis asynchronously."""
        value = await self.redis.get(key)
        return pickle.loads(value) if value else None

    async def exists(self, key: str) -> bool:
        """Check if a key exists in Redis asynchronously."""
        return await self.redis.exists(key)
    
    async def enqueue(self, key: str, value: Any) -> None:
        """Enqueue a value in Redis asynchronously."""
        await self.redis.lpush(key, pickle.dumps(value))
    
    async def dequeue(
        self, 
        key: str,
        block: bool = True
    ) -> Optional[Any]:
        """Dequeue a value from Redis asynchronously."""
        if block:
            value = await self.redis.blpop(key)
        else:
            value = await self.redis.lpop(key)
        return pickle.loads(value) if value else None
        
    async def dequeue_all(
        self, 
        key: str
    ) -> list[Any]:
        """Dequeue all values from Redis asynchronously."""
        values = await self.redis.lrange(key, 0, -1)
        return [pickle.loads(value) for value in values]
    
    async def llen(
        self,
        key: str
    ) -> int:
        """Get the length of a list in Redis asynchronously."""
        return await self.redis.llen(key)
    
    async def delete(self, key: str) -> None:
        """Delete a key from Redis asynchronously."""
        await self.redis.delete(key)

    async def clear(self) -> None:
        """Clear all keys in Redis asynchronously."""
        await self.redis.flushdb()
