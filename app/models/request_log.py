from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, index=True)
    method = Column(String)
    endpoint = Column(String)
    ip_address = Column(String)
    response_time = Column(Float)
    filename = Column(String, nullable=True) 
    student_name = Column(String, nullable=True)