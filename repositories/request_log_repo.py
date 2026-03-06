from sqlalchemy.orm import Session
from models.request_logs import RequestLog

def create_log(db: Session, log_data: dict):

    log = RequestLog(**log_data)

    db.add(log)
    db.commit()
    db.refresh(log)
    return log