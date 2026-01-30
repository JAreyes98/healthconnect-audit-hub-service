from sqlalchemy.orm import Session
import models
from dateutil import parser
import logging

def save_audit_event(db: Session, data: dict):
    new_log = models.AuditLog(
        timestamp_origin=parser.parse(data.get('timestamp')),
        service_name=data.get('service'),
        action=data.get('action'),
        details=data.get('details'),
        severity=data.get('severity', 'INFO')
    )
    db.add(new_log)
    db.commit()
    logging.info(f"Audit event saved: {new_log.id} ✅")
    return new_log