from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from core.database import Base


class RequestLog(Base):
    __tablename__="request_logs"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(String, index=True)
    path = Column(String)

    ip_address = Column(String)

    status_code = Column(Integer)
    status = Column(String)
    
    response_time = Column(Float)

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))








