from typing import Literal
from pydantic import BaseModel, Field
import uuid
import time

class Order(BaseModel):
    order_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str
    price: float
    quantity: float
    side: Literal["Buy", "Sell"]
    order_type: Literal["Limit", "Market"]
    order_receive_timestamp: float = Field(default_factory=lambda: time.time())
    status: str = "Pending"
    average_price: float = 0.0
    filled_qty: int = 0
    pending_qty: int = 0  
    order_place_timestamp: float = Field(default_factory=lambda: time.time())
    last_order_update_timestamp: float = Field(default_factory=lambda: time.time())
    message: str = "Order created successfully"

    def to_dict(self) -> dict:
        return self.dict()

