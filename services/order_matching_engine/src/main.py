import asyncio
import logging

from engine.order_matching_engine import OrderMatchingEngine
from cache.redis_manager import RedisManager


async def main():
    engine = OrderMatchingEngine()
    redis = RedisManager.get_instance()
    # Two different processes for different consumers like order_queue, market_data_queue.
    while True:
        try:
            order_data = await redis.order_lister()
            if order_data:
                await engine.process_order_queue(order_data)
        except Exception as e:
            logging.exception(f"Error processing order: {e}")
        
        
if __name__ == "__main__":
    logging.info("Starting order matching engine...")
    asyncio.run(main())