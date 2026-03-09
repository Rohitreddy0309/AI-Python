"""
Request logging middleware.

This module defines middleware that logs incoming HTTP requests,
including request ID, method, endpoint, client IP address,
and response time into the database.
"""

import time
import uuid

from sqlalchemy import text
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from core.database import SessionLocal


# pylint: disable=too-few-public-methods
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP request details to the database."""

    async def dispatch(self, request: Request, call_next):
        """
        Process incoming requests and log request details.

        Args:
            request (Request): Incoming HTTP request.
            call_next: Function to pass request to the next middleware or route.

        Returns:
            Response: HTTP response with request ID header added.
        """
        start_time = time.time()

        request_id = str(uuid.uuid4())
        method = request.method
        endpoint = request.url.path
        ip_address = request.client.host

        response: Response = await call_next(request)

        process_time = time.time() - start_time

        db = SessionLocal()

        db.execute(
            text(
                """
                INSERT INTO request_logs
                (request_id, method, endpoint, ip_address, response_time)
                VALUES (:request_id, :method, :endpoint, :ip_address, :response_time)
                """
            ),
            {
                "request_id": request_id,
                "method": method,
                "endpoint": endpoint,
                "ip_address": ip_address,
                "response_time": process_time,
            },
        )

        db.commit()
        db.close()

        response.headers["X-Request_ID"] = request_id

        return response
