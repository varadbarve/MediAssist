"""
Layer 9 — User Model for Authentication
Stores user accounts with bcrypt-hashed passwords.
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime, timezone
from app.db.base_class import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="staff")  # admin, doctor, staff
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
