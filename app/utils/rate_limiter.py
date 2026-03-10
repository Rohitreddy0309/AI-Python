import time
from fastapi import Request, HTTPException

# store requests
request_log = {}

MAX_REQUESTS = 10
TIME_WINDOW = 60   # seconds


async def rate_limiter(request: Request):

    user_ip = request.client.host
    current_time = time.time()

    if user_ip not in request_log:
        request_log[user_ip] = []

    # remove old requests
    request_log[user_ip] = [
        t for t in request_log[user_ip]
        if current_time - t < TIME_WINDOW
    ]

    if len(request_log[user_ip]) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Only 10 requests per minute allowed."
        )

    request_log[user_ip].append(current_time)