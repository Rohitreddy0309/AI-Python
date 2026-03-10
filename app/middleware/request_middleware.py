import time
import uuid
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.database import SessionLocal
from app.models.request_log import RequestLog

class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()
        request_id = str(uuid.uuid4())
        ip_address = request.client.host

        student_name = None
        file_name = None

        # Read request body
        try:
            body = await request.body()

            if body:
                data = json.loads(body)

                if "name" in data:
                    student_name = data["name"]

        except:
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
            student_name=student_name
        )

        db.add(log)
        db.commit()
        db.close()

        response.headers["X-Request-ID"] = request_id

        return response