from pydantic import BaseModel, Field
from datetime import datetime


class SensorBase(BaseModel):
    machine_id: str
    
    temperature: float = Field(..., ge=-50, le=200)
    pressure: float = Field(..., ge=0, le=500)
    vibration: float = Field(..., ge=0, le=100)
    humidity: float = Field(..., ge=0, le=100)
    voltage: float = Field(..., ge=0, le=500)
    current: float = Field(..., ge=0, le=100)


class SensorDataCreate(SensorBase):
    failure: int = Field(..., ge=0, le=1)


class PredictionRequest(SensorBase):
    pass
class PredictionResponse(BaseModel):
    prediction: int
    explanation: str
    probability:float