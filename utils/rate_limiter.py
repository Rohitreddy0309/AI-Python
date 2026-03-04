import time
from fastapi import Request, HTTPException


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
        raise HTTPException(
            status_code=429,
            detail = "Rate limit exceeded"
        )
    
    request_logs[ip].append(current_time)