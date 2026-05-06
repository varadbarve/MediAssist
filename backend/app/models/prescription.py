from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

class Prescription(Base):
    prescription_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patient.patient_id"))
    medicine_name = Column(String)
    dosage = Column(String)
    timing = Column(String)

    # In a real app, this might be linked to a specific report
