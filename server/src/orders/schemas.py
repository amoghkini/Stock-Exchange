from typing import Literal
from pydantic import BaseModel


class OrderCreateModel(BaseModel):
    baseAsset: str
    quoteAsset: str
    price: float
    quantity: float
    side: Literal["buy", "sell"]
    kind: str