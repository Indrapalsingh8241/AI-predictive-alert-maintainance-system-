from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app.models import SensorData
from backend.app.model_pred import PredictionLog
from backend.app.schemas import SensorBase,PredictionResponse
from backend.ai_explanation.app import generate_explanation
from backend.alerts.alert_engine import check_alert
from backend.alerts.telegram_alert import send_telegram_alert
from backend.services.prediction_service import predict_sensor
import joblib

model = joblib.load("/Users/indrapal/industrial_predictive_alert_system/backend/etl/model.pkl")
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {
        "message": "Industrial Predictive Alert System"
    }
@app.post("/sensor-data")
def add_sensor_data(
    sensor: SensorBase,
    db: Session = Depends(get_db)
):
    

    prediction, probability, explanation = predict_sensor(sensor)
  
    if probability >= 0.95:
        status = "STOPPED"

    elif probability >= 0.80:
            status = "WARNING"

    else:
        status = "RUNNING"
    log = PredictionLog(
        machine_id=sensor.machine_id,
    status=status,
   temperature=sensor.temperature,
    pressure=sensor.pressure,
    vibration=sensor.vibration,
    humidity=sensor.humidity,
    voltage=sensor.voltage,
    current=sensor.current,
    prediction=int(prediction),
    probability=float(probability),
    explanation = explanation
)
            

    db.add(log)
    db.commit()
    
    alert = check_alert(
        machine_id=sensor.machine_id,
        failure_probability=probability,
        explanation=explanation
    )

    if alert:
        send_telegram_alert(alert)
    
    return{
  "machine_id": sensor.machine_id,
    "status": status,
    "prediction": int(prediction),
    "probability": float(probability),
    "message": explanation
}
    

