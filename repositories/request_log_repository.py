from sqlalchemy.orm import Session
from models.request_log import RequestLog

class RequestLogRepository:
    @staticmethod
    def create_log(db: Session, log_data: dict):
        log = RequestLog(**log_data)

        db.add(log)
        db.commit()

        