from dataclasses import dataclass
from typing import Literal

from orderbook.order_side import OrderSide
from orderbook.order_type import OrderType


@dataclass
class Order:
    order_id: str
    symbol: str
    price: float
    quantity: float
    side: Literal[OrderSide.BUY, OrderSide.SELL]
    order_type: Literal[OrderType.LIMIT, OrderType.MARKET]
    order_receive_timestamp: float
    status: str
    average_price: float
    filled_qty: int
    pending_qty: int
    order_place_timestamp: float
    last_order_update_timestamp: float
    message: str
    
    def __hash__(self):
        return hash(self.order_id)
    
    def __str__(self) -> str:
        return f"order_id: {self.order_id}"