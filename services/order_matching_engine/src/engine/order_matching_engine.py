import logging
from orderbook.order import Order
from orderbook.orderbook import Orderbook

from cache.redis_manager import RedisManager


class OrderMatchingEngine:
    
    def __init__(self) -> None:
        self.orderbooks: dict[str, Order] = {}
        self.redis = RedisManager.get_instance()
        
    async def process_order_queue(
        self,
        order
    ):  
        # The payload should define the type such as create_order, cancel_order etc.
        # Based on the order type, create a data class from dict and pass it to orderbook.
        # We can have seaprate market data service connected to this engine which is responsible to return the market data. This is for adhoc requests. 
        # The engine should publish this data to pub sub channel which will then connect to websocket server.
        
        symbol: str = order["symbol"]
        logging.info(f"Processing order: {order}")
        if symbol not in self.orderbooks:
            self.orderbooks[symbol] = Orderbook(symbol)
        
        channel = f"order_fill:{order['order_id']}"
        await self.redis.send_to_trading_gateway(channel, order)
        await self.redis.redis.publish(channel, order)
        
        # Switch case based on order_type (create, amend, cancel)

    def process_market_data_queue(self):
        pass
    
    def get_snapshot(self):
        # This feature can be activated based on the env variable
        pass
    
    def replay_orders(self, timestamp):
        pass
    
    def write_snapshot(self):
        pass
    
    def prepare_new_order(self):
        pass
    
    def prepare_modify_order(self):
        pass
    
    def prepare_cancel_order(self):
        pass
    
    
    
    