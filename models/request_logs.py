from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from core.database import base


class RequestLog(base):
    __tablename__ = "request_logs"

    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(String, nullable=True)

    request_id = Column(String)
    endpoint = Column(String)
    ip_address = Column(String)

    status_code = Column(Integer)
    status_message = Column(String)

    response_time = Column(Float)

    created_at = Column(DateTime, server_default=func.now())