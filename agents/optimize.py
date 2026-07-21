from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
import uuid

# Initialize the Intervention Optimization Agent (Member 2)
app = FastAPI(title="Intervention Optimization Agent")

# ---------------------------------------------------------
# 1. Pydantic Models (Validation for Incoming Data)
# ---------------------------------------------------------
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

# This model strictly validates the incoming JSON from Member 1
class SourceIntelligenceData(BaseModel):
    request_id: Optional[str] = None
    agent_name: str
    city: str
    timestamp: str
    current_air_quality: CurrentAirQuality
    weather: Weather
    source_attribution: SourceAttribution
    hotspot_prediction: HotspotPrediction
    compliance_risk: ComplianceRisk

# ---------------------------------------------------------
# 2. Optimization Logic & API Endpoint
# ---------------------------------------------------------
@app.post("/receive-analysis")
async def receive_analysis(data: SourceIntelligenceData):
    try:
        # Generate Request ID if Member 1 didn't send one
        req_id = data.request_id or f"SIM_REQ_{uuid.uuid4().hex[:6].upper()}"
        
        # Optimization Logic based on incoming data
        aqi = data.current_air_quality.aqi
        dominant = data.source_attribution.dominant_source
        is_anomaly = aqi > 150
        adjustment = 45 if dominant == "Traffic" else 30
        
        # Construct the EXACT JSON structure for Member 3
        final_payload = {
            "request_id": req_id,
            "optimization_context": {
                "zone_id": f"{data.city.upper()}_ZONE_01",
                "is_anomaly_detected": is_anomaly
            },
            "simulation_inputs": {
                "traffic_light_adjustment_seconds": adjustment if is_anomaly else 0,
                "suggested_flow_rate": 0.85,
                "priority_level": "HIGH" if data.compliance_risk.risk_level == "Critical" else "LOW"
            },
            "analytical_metrics": {
                "predicted_pm_reduction_percent": 12.5,
                "congestion_index": 0.78
            },
            "simulation_instructions": {
                "run_mode": "stress_test",
                "duration_cycles": 10
            },
            "baseline_environmental_metrics": {
                "avg_aqi": aqi,
                "pm25": 115.5,
                "pm10": 240.0,
                "co": 2.4
            },
            "sub_zones": [
                { "sub_zone_id": f"{data.city.upper()}_ZONE_01_NORTH", "lat": 13.0827, "lng": 80.2707, "baseline_aqi": aqi + 7 },
                { "sub_zone_id": f"{data.city.upper()}_ZONE_01_SOUTH", "lat": 13.0067, "lng": 80.2206, "baseline_aqi": aqi + 32 },
                { "sub_zone_id": f"{data.city.upper()}_ZONE_01_EAST",  "lat": 13.0405, "lng": 80.2435, "baseline_aqi": aqi - 18 },
                { "sub_zone_id": f"{data.city.upper()}_ZONE_01_WEST",  "lat": 13.0644, "lng": 80.2001, "baseline_aqi": aqi + 67 }
            ]
        }
        
        # 3. Forward the generated payload to Member 3 (Simulation Agent)
        try:
            # Update this URL to match Member 3's live endpoint
            member3_url = "http://127.0.0.1:8000/agent_sim/run"
            requests.post(member3_url, json=final_payload)
            print(f"✅ Data forwarded to Simulation Agent (Member 3) with ID: {req_id}")
        except Exception as e:
            print(f"❌ Member 3 (Simulation Agent) not reachable: {e}")
            
        return final_payload

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
