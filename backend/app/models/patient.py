from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base
from app.core.encryption import encrypt_value, decrypt_value


class Patient(Base):
    patient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    age_group = Column(String)
    gender = Column(String)
    phone_number = Column(String)  # Stored encrypted via Fernet AES

    reports = relationship("Report", back_populates="patient")

    def set_phone(self, plain_phone: str):
        """Encrypt and store a phone number."""
        self.phone_number = encrypt_value(plain_phone)

    def get_phone(self) -> str:
        """Decrypt and return the phone number."""
        return decrypt_value(self.phone_number) if self.phone_number else ""
