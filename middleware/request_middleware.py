import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from models.request_log import RequestLog
from core.database import SessionLocal


class RequestMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        if request.url.path in ["/docs", "/openapi.json", "/redoc", "/favicon.ico"]:
            return await call_next(request)
        

        start_time = time.time()

        request_id = str(uuid.uuid4())

        ip_address = request.client.host

        path = request.url.path

        response = await call_next(request)

        process_time = time.time() - start_time

        status_map = {
            200: "Success",
            201: "Created",
            307: "Temporary Redirect",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            409: "Conflict",
            422: "Invalid Input",
            429: "Rate Limit Exceeded",
            500: "Server Error"
        }
        status_text = status_map.get(response.status_code, "Unknown")

        status_code = f"{response.status_code} {status_text}"
        

        db = SessionLocal()

        try:

            log = RequestLog(
                request_id=request_id,
                ip_address=ip_address,
                path=path,
                status_code=status_code,
                response_time=process_time

        )
        
            db.add(log)
            db.commit()
        finally:
            db.close()

        print(
            f"[REQUEST] {path} → {status_code} "
            f"({process_time:.4f}s) IP:{ip_address}"
        )

        


        response.headers["X-Request-ID"] = request_id

        return response