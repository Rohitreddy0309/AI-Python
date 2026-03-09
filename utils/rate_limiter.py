"""
Rate limiting utility.

This module implements a simple in-memory rate limiter that restricts
the number of requests a client can make within a defined time window.
"""

import time

from fastapi import HTTPException, Request

RATE_LIMIT = 10
TIME_WINDOW = 60

user_requests = {}


def rate_limiter(request: Request):
    """
    Enforce request rate limiting based on client IP address.

    Args:
        request (Request): Incoming HTTP request.

    Raises:
        HTTPException: If the client exceeds the allowed request limit.
    """
    client_ip = request.client.host
    current_time = time.time()

    if client_ip not in user_requests:
        user_requests[client_ip] = []

    user_requests[client_ip] = [
        t for t in user_requests[client_ip] if current_time - t < TIME_WINDOW
    ]

    if len(user_requests[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    user_requests[client_ip].append(current_time)
