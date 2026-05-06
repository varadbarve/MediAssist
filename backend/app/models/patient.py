from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

class Patient(Base):
    patient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    age_group = Column(String)
    gender = Column(String)
    phone_number = Column(String) # In a real app, this would be encrypted

    reports = relationship("Report", back_populates="patient")
