import random

def get_random_client_id():
    return "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=24))
