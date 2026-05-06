from pydantic import BaseModel
from typing import Optional
import uuid

class ReportBase(BaseModel):
    hemoglobin: Optional[float] = None
    cholesterol: Optional[float] = None
    vitamin_d: Optional[float] = None

class ReportCreate(ReportBase):
    patient_id: uuid.UUID

class Report(ReportBase):
    report_id: uuid.UUID
    patient_id: uuid.UUID