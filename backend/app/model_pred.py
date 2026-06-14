from sqlalchemy import Column, Integer, Float, DateTime, String
from datetime import datetime

from backend.app.database import Base, engine

class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True)

    machine_id = Column(String)
    status = Column(String)
    temperature = Column(Float)
    pressure = Column(Float)
    vibration = Column(Float)
    humidity = Column(Float)
    voltage = Column(Float)
    current = Column(Float)

    prediction = Column(Integer)
    probability = Column(Float)
    explanation = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)
