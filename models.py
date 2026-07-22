from database.connection import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="Public User") # Admin, Researcher, Public User
    is_active = Column(Boolean, default=True)

class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    description = Column(String, nullable=True)

class WeatherData(Base):
    __tablename__ = "weather_data"
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    wind_speed = Column(Float)
    visibility = Column(Float, nullable=True)
    rain = Column(Float, nullable=True)
    
    zone = relationship("Zone")

class AQIData(Base):
    __tablename__ = "aqi_data"
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    aqi = Column(Float)
    pm25 = Column(Float)
    pm10 = Column(Float)
    no2 = Column(Float)
    so2 = Column(Float)
    co = Column(Float)
    o3 = Column(Float)
    
    zone = relationship("Zone")

class SimulationHistory(Base):
    __tablename__ = "simulation_history"
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    interventions_applied = Column(JSON)
    initial_aqi = Column(Float)
    predicted_aqi = Column(Float)
    improvement_percent = Column(Float)
    ai_reasoning = Column(Text)
    
    zone = relationship("Zone")

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    target_time = Column(DateTime)
    predicted_aqi = Column(Float)
    confidence = Column(Float)

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    title = Column(String)
    description = Column(Text)
    priority = Column(String)
    expected_reduction = Column(Float)
    cost = Column(String)
    difficulty = Column(String)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)
    report_type = Column(String) # PDF, CSV
    url = Column(String)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    type = Column(String) # Alert, Info
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_read = Column(Boolean, default=False)
