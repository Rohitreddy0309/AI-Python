"""
Rate limiting utility.

This module implements a simple in-memory rate limiter that restricts
the number of requests a user (identified by IP address) can make
within a defined time window.
"""

import time

from fastapi import Request

from utils.exceptions import RateLimitExceeded


RATE_LIMIT = 10
WINDOW_SIZE = 60  # seconds

request_store = {}


def rate_limit(request: Request):
    """
    Enforce request rate limiting based on client IP address.

    This function tracks the timestamps of requests made by each client
    and ensures that the number of requests does not exceed the allowed
    limit within the defined time window.

    Args:
        request (Request): Incoming FastAPI request object.

    Raises:
        RateLimitExceeded: If the request limit is exceeded.
    """

    user_ip = request.client.host
    current_time = time.time()

    # Initialize user store
    if user_ip not in request_store:
        request_store[user_ip] = []

    # Remove timestamps older than the window size
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
