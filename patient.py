from pydantic import BaseModel, SecretStr
from typing import Optional
import uuid

class PatientBase(BaseModel):
    age_group: Optional[str] = None
    gender: Optional[str] = None
    phone_number: SecretStr

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    patient_id: uuid.UUID