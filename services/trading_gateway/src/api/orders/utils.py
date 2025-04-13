import random
import time


def generate_order_id() -> str:
    return f"{int(time.time())}_{random.randint(0, 1000)}"
