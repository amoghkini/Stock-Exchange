import redis
import os
    
def read_from_queue():
    

    queue = redis.Redis(
        host=os.getenv("QUEUE_REDIS_HOST", "exchange_redis"),
        port=int(os.getenv("QUEUE_REDIS_PORT", 6379)),
        db=0
    )
    print("Connected to Redis queue")
    while True:
        # Get the latest order from the queue (blocking read)
        order_data_json = queue.brpop("orders_queue")
        print("Order fetched from queue:", order_data_json)
        if order_data_json:
            print("Order fetched from queue:", order_data_json[1].decode())
            # Process the order here (convert from JSON if needed)

if __name__ == "__main__":
    print("Starting order matching engine...")
    read_from_queue()