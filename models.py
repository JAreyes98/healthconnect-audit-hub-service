from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base
import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp_origin = Column(DateTime)
    service_name = Column(String(50))
    action = Column(String(100))
    details = Column(Text)
    severity = Column(String(20))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)