from schemas import Inputs
from datetime import datetime

def calculate_age(birth_date: str) -> int:
    if not birth_date:
        return 0  # Default to 0 if birth date is missing
    year, month, day = map(int, birth_date.split('-'))
    born = datetime(year, month, day)
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def extract_age_from_ehr(ehr_data: dict) -> int:
    return calculate_age(ehr_data.get("birthDate", ""))

def extract_high_rate_from_observations(observations: list) -> int:
    entries = observations.get("entry", [])
    for entry in entries:
        resource = entry.get("resource", {})
        if resource.get("code", {}).get("coding", [{}])[0].get("code") == "8867-4":  # LOINC code for heart rate
            value = resource.get("valueQuantity", {}).get("value")
            if value and value > 100:  # Threshold for high heart rate
                return 1
    return 0

def extract_elevated_troponin(observations: list) -> int:
    entries = observations.get("entry", [])
    for entry in entries:
        resource = entry.get("resource", {})
        if resource.get("code", {}).get("coding", [{}])[0].get("code") == "6598-7":  # LOINC code for troponin
            value = resource.get("valueQuantity", {}).get("value")
            if value and value > 0.04:  # Threshold for elevated troponin
                return 1
    return 0

def has_condition(conditions: list, condition_code: str) -> int:
    entries = conditions.get("entry", [])
    for entry in entries:
        resource = entry.get("resource", {})
        if resource.get("code", {}).get("coding", [{}])[0].get("code") == condition_code:
            return 1
    return 0

def build_ehr_features(patient: dict, observations: dict, conditions: dict) -> dict:
    return {
        "age": extract_age_from_ehr(patient),
        "elevated_troponin": extract_elevated_troponin(observations),
        "ecg_abnormalities": has_condition(conditions, "I48"),  # Atrial fibrillation ~ ECG abnormalities
        "hypertension": has_condition(conditions, ["hypertension"]), # code I10
        "diabetes": has_condition(conditions, ["diabetes"]), # code E11
        "smoking": has_condition(conditions, ["smoking", "nicotine"]), # code F17
        "heart_disease_history": has_condition(conditions, ["coronary_artery_disease", "myocardial_infarction", "heart_disease", "cardiovascular_disease"]), # code I25
        "high_heart_rate": extract_high_rate_from_observations(observations)
    }


def combine_form_and_ehr(form_data: dict, ehr_data: dict) -> Inputs:
    combined_data = {
        "age": ehr_data.get("age", form_data.get("age")),
        "chest_pain": form_data.get("chest_pain", 0),
        "shortness_of_breath": form_data.get("shortness_of_breath", 0),
        "radiating_pain": form_data.get("radiating_pain", 0),
        "elevated_troponin": ehr_data.get("elevated_troponin", form_data.get("elevated_troponin")),
        "ecg_abnormalities": ehr_data.get("ecg_abnormalities", form_data.get("ecg_abnormalities")),
        "hypertension": ehr_data.get("hypertension", form_data.get("hypertension")),
        "diabetes": ehr_data.get("diabetes", form_data.get("diabetes")),
        "smoking": ehr_data.get("smoking", form_data.get("smoking")),
        "heart_disease_history": ehr_data.get("heart_disease_history", form_data.get("heart_disease_history")),
        "high_heart_rate": ehr_data.get("high_heart_rate", form_data.get("high_heart_rate"))
    }

    return Inputs(**combined_data)