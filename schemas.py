from pydantic import BaseModel
from typing import Optional

class Inputs(BaseModel):
    # input data provided by patient
    chest_pain: int
    shortness_of_breath: int
    radiating_pain: int

    # structured data from EHR
    age: int # Patient
    elevated_troponin: int # Observation
    ecg_abnormalities: int
    hypertension: int # Condition
    diabetes: int # Condition
    smoking: int 
    heart_disease_history: int # Condition
    high_heart_rate: int # Observation


    # FHIR data
    patient_id: Optional[str] = None

class SymptomInput(BaseModel): #input only
    chest_pain: int
    shortness_of_breath: int
    radiating_pain: int