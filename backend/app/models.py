from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime

from backend.app.database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True)

    temperature = Column(Float)
    pressure = Column(Float)
    vibration = Column(Float)
    humidity = Column(Float)
    voltage = Column(Float)
    current = Column(Float)

    failure = Column(Integer)

    timestamp = Column(DateTime, default=datetime.utcnow)