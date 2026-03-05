import time
from fastapi import HTTPException

user_requests = {}

LIMIT = 10
WINDOW = 60


def rate_limiter(user_id: int):

    current_time = time.time()

    if user_id not in user_requests:
        user_requests[user_id] = []

    request_times = user_requests[user_id]

    request_times = [
        t for t in request_times
        if current_time - t < WINDOW
    ]

    user_requests[user_id] = request_times

    if len(request_times) >= LIMIT:

        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )

    user_requests[user_id].append(current_time)