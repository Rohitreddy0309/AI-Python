"""Simple in-memory rate limiter for incoming requests."""

import time

from fastapi import Request

from utils.exceptions import RateLimitExceeded

RATE_LIMIT = 10
WINDOW = 60

# Track request timestamps by client IP.
user_requests = {}


def rate_limiter(request: Request):
    """Enforce a simple fixed-window rate limit per client IP."""

    ip = request.client.host
    current_time = time.time()

    if ip not in user_requests:
        user_requests[ip] = []

    requests = user_requests[ip]

    # Remove requests outside the current rate-limit window.
    user_requests[ip] = [
        req_time for req_time in requests if current_time - req_time < WINDOW
    ]

    if len(user_requests[ip]) >= RATE_LIMIT:
        raise RateLimitExceeded()

    user_requests[ip].append(current_time)
