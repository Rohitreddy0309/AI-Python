"""
Simple in-memory rate limiting utility.

This module limits the number of requests a user can make within
a specified time window using an in-memory dictionary to track
request timestamps.
"""

import time

from fastapi import HTTPException

user_requests = {}

LIMIT = 10
WINDOW = 60


def rate_limiter(user_id: int):
    """
    Enforces rate limiting for a specific user.

    Allows only a fixed number of requests (LIMIT) within a
    defined time window (WINDOW). If the limit is exceeded,
    an HTTPException with status code 429 is raised.

    Args:
        user_id (int): Unique identifier of the user making the request.

    Raises:
        HTTPException: If the user exceeds the allowed request limit.
    """

    current_time = time.time()

    if user_id not in user_requests:
        user_requests[user_id] = []

    request_times = user_requests[user_id]

    request_times = [t for t in request_times if current_time - t < WINDOW]

    user_requests[user_id] = request_times

    if len(request_times) >= LIMIT:

        raise HTTPException(
            status_code=429, detail="Rate limit exceeded. Try again later."
        )

    user_requests[user_id].append(current_time)
