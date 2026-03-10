"""Middleware to log incoming requests and persist request metadata."""

import time
import uuid

from fastapi import Request
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from core.config import logger
from core.db import SessionLocal
from models.request_logs import RequestLog


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs request details and stores them in the database."""

    async def dispatch(self, request: Request, call_next):
        """Wrap request processing to add logging and request tracking."""

        request_id = str(uuid.uuid4())
        start_time = time.time()

        ip_address = request.client.host
        method = request.method
        path = request.url.path

        response = await call_next(request)

        process_time = time.time() - start_time

        db: Session = SessionLocal()

        try:
            log = RequestLog(
                request_id=request_id,
                method=method,
                path=path,
                ip_address=ip_address,
                response_time=process_time,
            )

            db.add(log)
            db.commit()

        except Exception as exc:
            logger.error("Failed to store request log: %s", exc)

        finally:
            db.close()

        # Expose the request id to clients for tracing.
        response.headers["X-Request-ID"] = request_id

        logger.info(
            "%s %s | %s | %.4fs | %s",
            method,
            path,
            ip_address,
            process_time,
            request_id,
        )

        return response
