from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Intervention Optimization Agent")

# 1. Define the models that match Member 1's JSON exactly
class CurrentAirQuality(BaseModel):
    aqi: int

class Weather(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: str

class SourceContribution(BaseModel):
    source: str
    contribution_percent: float

class SourceAttribution(BaseModel):
    dominant_source: str
    source_contributions: List[SourceContribution]

class Hotspot(BaseModel):
    location: str
    predicted_aqi: int
    risk_level: str

class HotspotPrediction(BaseModel):
    highest_risk_hotspot: Hotspot
    all_hotspots: List[Hotspot]

class ComplianceRisk(BaseModel):
    risk_score: int
    risk_level: str

# This is the "Data Package" Member 1 sends to you
class SourceIntelligenceData(BaseModel):
    agent_name: str
    city: str
    timestamp: str
    current_air_quality: CurrentAirQuality
    weather: Weather
    source_attribution: SourceAttribution
    hotspot_prediction: HotspotPrediction
    compliance_risk: ComplianceRisk

# 2. The API Endpoint that Member 1 will call
@app.post("/optimize")
async def process_pollution_data(data: SourceIntelligenceData):
    try:
        # Now you can use dot notation like data.city, data.current_air_quality.aqi
        aqi = data.current_air_quality.aqi
        dominant = data.source_attribution.dominant_source
        target = data.hotspot_prediction.highest_risk_hotspot.location

        # Logic to decide the action
        action = "Monitor normal flow"
        adjustment = 0
        
        if aqi > 150:
            if dominant == "Traffic":
                action = f"Reduce traffic in {target}"
                adjustment = 20
            else:
                action = "Deploy industrial cleaning trucks"

        # Return the "Decision Package" for Member 3
        return {
            "status": "Optimization Completed",
            "decision": {
                "action": action,
                "adjustment_seconds": adjustment,
                "target_location": target
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
