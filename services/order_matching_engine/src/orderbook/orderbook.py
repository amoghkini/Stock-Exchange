import logging


class Orderbook:
    
    
    def __init__(
        self,
        symbol: str
    ) -> None:
        self.symbol = symbol
        self.bids = {}
        self.asks = []
        # Make sure we read snapshot and replay messages before we start listning anything on this book.
        logging.info(f"Orderbook created for {self.symbol}")
        
    def add_order(self, order):
        pass
    
    def modify_order(self, order_modification_params):
        pass
    
    def cancel_order(self):
        # Call cancel_bid or cancel_ask based on order type
        pass
    
    def match_bid(self):
        pass
    
    def match_ask(self):
        pass
    
    def get_depth(self):
        pass
    
    def get_best_bid(self):
        pass
    
    def best_ask(self):
        pass
    
    def get_last_traded_price(self):
        self.get_last_traded_order()
    
    def get_last_traded_order(self):
        pass
    
    def get_open_orders(self, user_id):
        pass
    
    def cancel_bid(self, order_id):
        pass
    
    def cancel_ask(self, order_id):
        pass
    
    def get_l1_book(self):
        pass
    
    def get_l2_book(self):
        pass

    