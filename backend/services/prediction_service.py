import joblib
from backend.ai_explanation.app import generate_explanation

import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "etl",
    "model.pkl"
)

model = joblib.load(MODEL_PATH)

def predict_sensor(sensor):
    risk_score = (
        (sensor.temperature > 85)
        + (sensor.vibration > 6)
        + (sensor.pressure > 40)
    )

    temp_vibration = sensor.temperature * sensor.vibration
    power = sensor.voltage * sensor.current
    temp_pressure_ratio = sensor.temperature / (sensor.pressure + 1)

    features = [[
        sensor.temperature,
        sensor.pressure,
        sensor.vibration,
        sensor.humidity,
        sensor.voltage,
        sensor.current,
        risk_score,
        temp_vibration,
        power,
        temp_pressure_ratio
    ]]

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    explanation = generate_explanation(sensor, prediction)

    return prediction, probability, explanation