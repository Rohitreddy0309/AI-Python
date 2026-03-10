"""ORM model for recording request logs."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from core.db import Base


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, index=True)
    method = Column(String)
    path = Column(String)
    ip_address = Column(String)
    response_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
