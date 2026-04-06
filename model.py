import math
from schemas import Inputs

#figure out weigths
WEIGHTS = {
    "intercept": -5.0,
    "chest_pain": 1.2,
    "shortness_of_breath": 0.8,
    "radiating_pain": 0.7,
    "age": 0.05,
    "elevated_troponin": 2.0,
    "ecg_abnormalities": 1.7,
    "hypertension": 0.6,
    "diabetes": 0.6,
    "smoking": 0.5,
    "heart_disease_history": 1.5,
    "high_heart_rate": 0.6,
}

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def compute_x(inputs: Inputs):
    x = WEIGHTS["intercept"]
    x += WEIGHTS["chest_pain"] * inputs.chest_pain
    x += WEIGHTS["shortness_of_breath"] * inputs.shortness_of_breath
    x += WEIGHTS["radiating_pain"] * inputs.radiating_pain
    x += WEIGHTS["age"] * inputs.age
    x += WEIGHTS["elevated_troponin"] * inputs.elevated_troponin
    x += WEIGHTS["ecg_abnormalities"] * inputs.ecg_abnormalities
    x += WEIGHTS["hypertension"] * inputs.hypertension
    x += WEIGHTS["diabetes"] * inputs.diabetes
    x += WEIGHTS["smoking"] * inputs.smoking
    x += WEIGHTS["heart_disease_history"] * inputs.heart_disease_history
    x += WEIGHTS["high_heart_rate"] * inputs.high_heart_rate
    return x

#determine risk category bounds
def risk_category(riskScore):
    if riskScore < 0.3:
        return "low"
    elif riskScore < 0.6:
        return "medium"
    else:
        return "high"

def predict_risk(inputs: Inputs):
    x = compute_x(inputs)
    riskScore = sigmoid(x)
    category = risk_category(riskScore)
    return {"Risk Score": riskScore, "Risk Category": category}