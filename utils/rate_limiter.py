"""
Simple in-memory rate limiter.

Limits the number of requests from a single IP
within a defined time window.
"""

import time
from fastapi import Request

from core.exceptions.custom_exception import RateLimitException


RATE_LIMIT = 10  # requests allowed
WINDOW = 60  # time window in seconds

request_logs = {}


def rate_limiter(request: Request):
    """Limit requests per IP address within a time window."""

    ip = request.client.host
    current_time = time.time()

    if ip not in request_logs:
        request_logs[ip] = []

    request_logs[ip] = [
        timestamp
        for timestamp in request_logs[ip]
        if current_time - timestamp < WINDOW
    ]

    if len(request_logs[ip]) >= RATE_LIMIT:
        raise RateLimitException()

    request_logs[ip].append(current_time)
