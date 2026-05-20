"""
Layer 6 — Audit Log Database Model
Stores audit events in the database for querying and compliance.
"""

from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime, timezone
from app.db.base_class import Base


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    event_type = Column(String(50), nullable=False, index=True)  # AUTH, REPORT_UPLOAD, CALL, etc.
    ip_address = Column(String(45))  # IPv6 max length
    patient_id_hash = Column(String(64))  # SHA-256 hash, not raw patient ID
    user_email = Column(String(255))  # Email of the user who triggered the event
    action = Column(String(100), nullable=False)  # e.g., login_success, report_processed
    details = Column(Text)  # Additional context
    status = Column(String(20), default="success")  # success / failure
