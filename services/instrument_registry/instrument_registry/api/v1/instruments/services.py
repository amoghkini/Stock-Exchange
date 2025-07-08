import logging

from instrument_registry.cache.redis_manager import RedisManager


redis = RedisManager.get_instance()

class InstrumentService:
    
    def __init__(self) -> None:
        logging.info("Initializing InstrumentService")