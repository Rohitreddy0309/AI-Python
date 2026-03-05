import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from core.database import SessionLocal
from repositories.request_log_repository import RequestLogRepository


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        path = request.url.path
        method = request.method

        # Ignore swagger / system routes
        ignore_paths = ["/", "/docs", "/openapi.json", "/favicon.ico", "/redoc"]

        # Only log real API operations
        allowed_methods = ["GET", "POST", "PUT", "DELETE"]

        if path not in ignore_paths and method in allowed_methods:

            request_id = str(uuid.uuid4())
            ip_address = request.client.host

            status_meanings = {
                200: "Successful Request",
                201: "Resource Created",
                400: "Invalid Input",
                404: "Resource Not found",
                500: "Internal Server Error"
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
                    "response_time": process_time   
                }

                RequestLogRepository.create_log(db, log_data)

            
            finally:
                db.close()

        
        return response
    


    



