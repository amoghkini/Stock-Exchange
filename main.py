from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Literal, Optional
import random
import logging

app = FastAPI()

BASE_ASSET = 'BTC'
QUOTE_ASSET = 'USD'
GLOBAL_TRADE_ID = 0

orderbook = {'bids': [], 'asks': []}
book_with_quantity = {'bids': {}, 'asks': {}}

class Fill(BaseModel):
    price: float
    qty: float
    tradeId: int

class Order(BaseModel):
    baseAsset: str
    quoteAsset: str
    price: float
    quantity: float
    side: Literal['buy', 'sell']
    kind: Optional[Literal['ioc']]

@app.post("/api/v1/order")
async def place_order(order: Order):
    global GLOBAL_TRADE_ID
    if order.baseAsset != BASE_ASSET or order.quoteAsset != QUOTE_ASSET:
        raise HTTPException(status_code=400, detail="Invalid base or quote asset")

    order_id = get_order_id()
    executed_qty, fills = fill_order(order_id, order.price, order.quantity, order.side, order.kind)
    return {"orderId": order_id, "executedQty": executed_qty, "fills": fills}


def get_order_id() -> str:
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=24))


def fill_order(order_id: str, price: float, quantity: float, side: str, kind: Optional[str] = None):
    global GLOBAL_TRADE_ID
    fills = []
    executed_qty = 0
    max_fill_quantity = get_fill_amount(price, quantity, side)

    # if kind == 'ioc' and max_fill_quantity < quantity:
    #     return 0, []

    orders = orderbook['asks'] if side == 'buy' else orderbook['bids']
    for o in orders[:]:
        if (side == 'buy' and o['price'] <= price) or (side == 'sell' and o['price'] >= price):
            filled_qty = min(quantity, o['quantity'])
            o['quantity'] -= filled_qty
            fills.append(Fill(price=o['price'], qty=filled_qty, tradeId=GLOBAL_TRADE_ID))
            GLOBAL_TRADE_ID += 1
            executed_qty += filled_qty
            quantity -= filled_qty
            if o['quantity'] == 0:
                orders.remove(o)
            if quantity == 0:
                break

    if quantity > 0:
        new_order = {"price": price, "quantity": quantity, "side": side, "orderId": order_id}
        orderbook['bids' if side == 'buy' else 'asks'].append(new_order)
        book_with_quantity['bids' if side == 'buy' else 'asks'][price] = quantity
    from pprint import pprint
    pprint(orderbook)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    pprint(book_with_quantity)
    return executed_qty, fills


def get_fill_amount(price: float, quantity: float, side: str) -> float:
    filled = 0
    orders = orderbook['asks'] if side == 'buy' else orderbook['bids']
    for o in orders:
        if (side == 'buy' and o['price'] <= price) or (side == 'sell' and o['price'] >= price):
            filled += min(quantity, o['quantity'])
    return filled
