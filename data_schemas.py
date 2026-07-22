from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ZoneSchema(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class WeatherDataSchema(BaseModel):
    id: int
    zone_id: int
    timestamp: datetime
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    visibility: Optional[float] = None
    rain: Optional[float] = None
    
    class Config:
        from_attributes = True

class AQIDataSchema(BaseModel):
    id: int
    zone_id: int
    timestamp: datetime
    aqi: float
    pm25: float
    pm10: float
    no2: float
    so2: float
    co: float
    o3: float
    
    class Config:
        from_attributes = True

class CombinedDataSchema(BaseModel):
    aqi_data: AQIDataSchema
    weather_data: WeatherDataSchema

class SimulationHistorySchema(BaseModel):
    id: int
    zone_id: int
    timestamp: datetime
    interventions_applied: List[str]
    initial_aqi: float
    predicted_aqi: float
    improvement_percent: float
    ai_reasoning: str
    
    class Config:
        from_attributes = True

class RecommendationSchema(BaseModel):
    id: int
    zone_id: int
    title: str
    description: str
    priority: str
    expected_reduction: float
    cost: str
    difficulty: str
    
    class Config:
        from_attributes = True

class ReportSchema(BaseModel):
    id: int
    filename: str
    generated_at: datetime
    report_type: str
    url: str
    
    class Config:
        from_attributes = True

class NotificationSchema(BaseModel):
    id: int
    message: str
    type: str
    created_at: datetime
    is_read: bool
    
    class Config:
        from_attributes = True
