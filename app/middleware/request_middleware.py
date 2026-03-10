"""
request_logging_middleware.py

This module defines a custom Starlette/FastAPI middleware to log
incoming HTTP requests into the database. Each request is assigned
a unique request ID and logged with metadata such as endpoint,
HTTP method, IP address, response time, and optional student/file info.

The middleware also attaches the request ID to the response headers
for traceability.
"""

import json
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.database import SessionLocal
from app.models.request_log import RequestLog


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests to the database.

    Attributes:
        None
    """

    async def dispatch(self, request: Request, call_next):
        """
        Processes each incoming request:
        1. Records start time and generates a unique request ID.
        2. Extracts client IP address.
        3. Attempts to parse request body for 'name' field.
        4. Calls the next middleware or endpoint.
        5. Measures response time.
        6. Stores a RequestLog entry in the database.
        7. Adds 'X-Request-ID' header to the response.

        Args:
            request (Request): Incoming HTTP request object.
            call_next (Callable): Function to call the next middleware or endpoint.

        Returns:
            Response: The HTTP response object with added request ID header.
        """
        start_time = time.time()
        request_id = str(uuid.uuid4())
        ip_address = request.client.host

        student_name = None
        file_name = None

        try:
            body = await request.body()

            if body:
                data = json.loads(body)

                if "name" in data:
                    student_name = data["name"]

        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

        response = await call_next(request)

        process_time = time.time() - start_time

        db = SessionLocal()

        log = RequestLog(
            request_id=request_id,
            endpoint=request.url.path,
            method=request.method,
            ip_address=ip_address,
            response_time=process_time,
            filename=file_name,
            student_name=student_name,
        )

        db.add(log)
        db.commit()
        db.close()

        response.headers["X-Request-ID"] = request_id

        return response
