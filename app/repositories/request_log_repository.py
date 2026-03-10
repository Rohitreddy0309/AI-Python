from sqlalchemy.orm import Session
from app.models.request_log import RequestLog


class RequestLogRepository:

    def create_log(
        self,
        db: Session,
        request_id: str,
        method: str,
        endpoint: str,
        ip_address: str,
        response_time: float
    ):
        log = RequestLog(
            request_id=request_id,
            method=method,
            endpoint=endpoint,
            ip_address=ip_address,
            response_time=response_time
        )

        db.add(log)
        db.commit()