from http.client import HTTPException

from fastapi import FastAPI, Body
from schemas import Inputs, SymptomInput
from model import predict_risk
from fhir_utils import (search_patients, get_patient_data, get_observations, get_conditions)
from feature_builder import build_ehr_features, combine_form_and_ehr

app = FastAPI(title="TriageAssist API")

@app.get("/")

def root():
    return {"message": "TriageAssist API is running"}

@app.post("/predict")
def predict(input: Inputs):
    return predict_risk(input)

@app.post("/predictFromFHIR/{patient_id}")
def predict_from_fhir(patient_id: str, form_data: SymptomInput = Body(...)):
    try:
        patient_data = get_patient_data(patient_id)
        observations = get_observations(patient_id)
        conditions = get_conditions(patient_id)

        ehr_data = build_ehr_features(patient_data, observations, conditions)
        combined_input = combine_form_and_ehr(form_data.dict(), ehr_data)
        combined_input.patient_id = patient_id
        return {
            "ehr_data": ehr_data,
            "combined_input": combined_input.dict(),
            "prediction": predict_risk(combined_input)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fhir/patients")
def fhir_patients(name: str | None = None, count: int = 5):
    try:
        return search_patients(name = name, count = count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # from fhir_utils import search_patients
    # return search_patients(name, count)

@app.get("/fhir/patient/{patient_id}")
def fhir_patient(patient_id: str):
    try:
        return get_patient_data(patient_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/fhir/patient/{patient_id}/observations")
def fhir_patient_observations(patient_id: str, count: int = 50):
    try:
        return get_observations(patient_id, count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/fhir/patient/{patient_id}/conditions")
def fhir_patient_conditions(patient_id: str, count: int = 50):
    try:
        return get_conditions(patient_id, count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fhir/features/{patient_id}")
def fhir_patient_features(patient_id: str):
    patient_data = get_patient_data(patient_id)
    observations = get_observations(patient_id)
    conditions = get_conditions(patient_id)

    ehr_data = build_ehr_features(patient_data, observations, conditions)
    return ehr_data