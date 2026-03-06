import time
from fastapi import Request
from utils.exceptions import RateLimitExceeded

RATE_LIMIT = 10
WINDOW_SIZE = 60   #Seconds

request_store = {}

def rate_limit(request: Request):
    user_ip = request.client.host
    current_time = time.time()
    
    # Initialize user store
    if user_ip not in request_store:
        request_store[user_ip] = []

    # Remove timestamps older than 60 seconds
    request_store[user_ip] = [
        timestamp
        for timestamp in request_store[user_ip]
        if current_time - timestamp < WINDOW_SIZE
    ]

    # Check rate limit
    if len(request_store[user_ip]) >= RATE_LIMIT:
        raise RateLimitExceeded(
            "Rate limit exceeded. Only 10 requests per minute allowed."
        )
    
    # Add current request timestamp
    request_store[user_ip].append(current_time)


    




