from sqlalchemy import Column, Float, ForeignKey, UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

class Report(Base):
    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patient.patient_id"))
    hemoglobin = Column(Float)
    cholesterol = Column(Float)
    vitamin_d = Column(Float)

    patient = relationship("Patient", back_populates="reports")
