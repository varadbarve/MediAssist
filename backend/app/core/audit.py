"""
Layer 6 — Audit Logging
Structured audit logger for tracking all security-relevant events.
Uses Python's built-in logging module (zero cost).
Patient IDs are SHA-256 hashed in logs to prevent PII leakage.
"""

import logging
import hashlib
import os
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler


# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Configure the audit logger
audit_logger = logging.getLogger("mediassist.audit")
audit_logger.setLevel(logging.INFO)

# Rotating file handler: 5MB per file, keep 5 backups
file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "audit.log"),
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
)
audit_logger.addHandler(file_handler)

# Console handler for development
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("[AUDIT] %(asctime)s | %(message)s", datefmt="%H:%M:%S")
)
audit_logger.addHandler(console_handler)


def _hash_patient_id(patient_id: str) -> str:
    """SHA-256 hash a patient ID for safe logging (no PII in logs)."""
    if not patient_id:
        return "unknown"
    return hashlib.sha256(patient_id.encode()).hexdigest()[:16]


def log_event(
    event_type: str,
    action: str,
    ip_address: str = "unknown",
    patient_id: str = "",
    details: str = "",
    status: str = "success",
    user_email: str = ""
):
    """
    Log a security-relevant audit event.

    Args:
        event_type: Category (e.g., 'AUTH', 'REPORT_UPLOAD', 'CALL', 'WEBHOOK')
        action: What happened (e.g., 'login_success', 'report_processed')
        ip_address: Client IP address
        patient_id: Patient ID (will be hashed in logs)
        details: Additional context
        status: 'success' or 'failure'
        user_email: Email of the authenticated user performing the action
    """
    patient_hash = _hash_patient_id(patient_id) if patient_id else "N/A"
    user_info = f" | user={user_email}" if user_email else ""

    message = (
        f"event={event_type} | action={action} | status={status} | "
        f"ip={ip_address} | patient_hash={patient_hash}{user_info}"
    )

    if details:
        message += f" | details={details}"

    if status == "failure":
        audit_logger.warning(message)
    else:
        audit_logger.info(message)

    # Write to database (Layer 6)
    try:
        from app.db.session import SessionLocal
        from app.models.audit_log import AuditLog
        
        db = SessionLocal()
        try:
            db_log = AuditLog(
                event_type=event_type,
                ip_address=ip_address,
                patient_id_hash=_hash_patient_id(patient_id) if patient_id else None,
                user_email=user_email,
                action=action,
                details=details,
                status=status
            )
            db.add(db_log)
            db.commit()
        finally:
            db.close()
    except Exception as e:
        # Don't crash the application if database logging fails
        print(f"[SECURITY WARNING] Failed to write audit log to database: {e}")

