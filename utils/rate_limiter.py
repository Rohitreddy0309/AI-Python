import time
from fastapi import Request
from core.exceptions.custom_exceptions import RateLimitException


RATE_LIMIT = 10         #requests allowed

WINDOW = 60             #time in seconds

request_logs = {}

def rate_limiter(request: Request):

    ip = request.client.host

    current_time = time.time()

    if ip not in request_logs:
        request_logs[ip] = []

    request_logs[ip] = [
        timestamp for timestamp in request_logs[ip]
        if current_time - timestamp < WINDOW
    ]

    if len(request_logs[ip]) >= RATE_LIMIT:
        raise RateLimitException()
    
    
    request_logs[ip].append(current_time)