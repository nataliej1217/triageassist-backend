# def get_patient_data_from_fhir(patient_id: str):
#     # Placeholder function to simulate fetching patient data from FHIR server
#     return {
#         "age": 65,
#         "elevated_troponin": 1,
#         "ecg_abnormalities": 1,
#         "hypertension": 1,
#         "diabetes": 0,
#         "smoking": 1,
#         "heart_disease_history": 1,
#         "high_heart_rate": 1
#     }

import os
import requests

FHIR_BASE_URL = os.getenv("FHIR_BASE_URL", "https://r4.smarthealthit.org/") #DOUBLE CHECK THIS URL 

def fhir_get(path:str, params:dict | None = None):
    url = f"{FHIR_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

    # try:
    #     response = requests.get(url, params=params)
    #     response.raise_for_status()
    #     return response.json()
    # except requests.RequestException as e:
    #     print(f"Error fetching data from FHIR server: {e}")
    #     return None


def search_patients(name: str | None = None, count: int = 5):
    params = {"_count": count}
    if name:
        params["name"] = name
    return fhir_get("Patient", params={"name": name})

def get_patient_data(patient_id: str):
    return fhir_get(f"Patient/{patient_id}")

def get_observations(patient_id: str, count: int = 50):
    return fhir_get("Observation", params={"patient": patient_id, "_count": count})

def get_conditions(patient_id: str, count: int = 50):
    return fhir_get("Condition", params={"patient": patient_id, "_count": count})