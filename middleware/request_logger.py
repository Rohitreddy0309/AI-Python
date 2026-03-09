"""
Request logging middleware.

This middleware captures incoming HTTP requests, measures
response time, collects request metadata, and stores logs
in the database for monitoring and debugging purposes.
"""

# pylint: disable=too-many-locals,too-few-public-methods

import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from core.database import SessionLocal
from repositories.request_log_repository import RequestLogRepository


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs API request information.

    Captures:
    - request ID
    - request path
    - client IP address
    - HTTP status code
    - response time
    """

    async def dispatch(self, request: Request, call_next):
        """Process the incoming request and log request details."""

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        path = request.url.path
        method = request.method

        # Ignore Swagger and system endpoints
        ignore_paths = ["/", "/docs", "/openapi.json", "/favicon.ico", "/redoc"]

        # Only log actual API operations
        allowed_methods = ["GET", "POST", "PUT", "DELETE"]

        if path not in ignore_paths and method in allowed_methods:
            request_id = str(uuid.uuid4())
            ip_address = request.client.host

            status_meanings = {
                200: "Successful Request",
                201: "Resource Created",
                400: "Invalid Input",
                404: "Resource Not Found",
                500: "Internal Server Error",
            }

            status = status_meanings.get(response.status_code, "Unknown")

            db = SessionLocal()

            try:
                log_data = {
                    "request_id": request_id,
                    "path": path,
                    "ip_address": ip_address,
                    "status_code": response.status_code,
                    "status": status,
                    "response_time": process_time,
                }

                RequestLogRepository.create_log(db, log_data)

            finally:
                db.close()

        return response
