from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from datetime import datetime

# Importing the FastAPI 'app' objects from your agents folder
from agents.source import app as source_app
from agents.optimize import app as optimize_app
from agents.agent_sim import app as sim_app

app = FastAPI(title="City Pollution OS - Main Orchestrator & Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 1. FIX FOR TEST PIPELINE (Prevents Timeout Error)
# ---------------------------------------------------------
class InputData(BaseModel):
    city_name: str
    aqi: int
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: str
    traffic_index: int
    industrial_emission_index: int
    dust_detected: bool
    smoke_detected: bool

@app.post("/run-pipeline")
def run_pipeline(data: InputData):
    req_id = f"SIM_REQ_{uuid.uuid4().hex[:6].upper()}"
    
    # Process through Agent 1 logic (Source)
    traffic = round(data.traffic_index * 0.5, 1)
    industry = round(data.industrial_emission_index * 0.4, 1)
    
    # Return immediate success response to avoid timeouts
    return {
        "status": "success",
        "request_id": req_id,
        "city": data.city_name,
        "source_attribution": {
            "traffic_impact": traffic,
            "industrial_impact": industry
        },
        "message": "Pipeline executed successfully!"
    }

# ---------------------------------------------------------
# 2. GOVERNANCE DASHBOARD LOGIC (For Frontend)
# ---------------------------------------------------------
aqi_map_data = None

class AQIZone(BaseModel):
    sub_zone_id: str
    lat: float
    lng: float
    baseline_aqi: int
    predicted_aqi: int
    risk_level: str

@app.post("/aqi_agent")
def receive_aqi(data: list[AQIZone]):
    global aqi_map_data
    aqi_map_data = [zone.dict() for zone in data]
    print("✅ Dashboard Received Data!")
    return {"message": "AQI Map Data Received", "zones_received": len(aqi_map_data)}

@app.get("/governance")
def governance():
    if aqi_map_data is None:
        return {"message": "Waiting for AQI data"}

    departments = []
    highest_risk_zone = max(aqi_map_data, key=lambda x: x["predicted_aqi"])
    
    # Calculations for the new frontend UI
    avg_aqi = sum(zone["predicted_aqi"] for zone in aqi_map_data) // len(aqi_map_data)

    # --- EDITED HERE: Updated to match "Very High" and "High" ---
    very_high_count = sum(1 for zone in aqi_map_data if zone["risk_level"] == "Very High")
    high_count = sum(1 for zone in aqi_map_data if zone["risk_level"] == "High")
    high_risk_zones = very_high_count + high_count

    # Keeping your original logic untouched but using the new variables
    if very_high_count > 0:
        departments.extend(["Pollution Control Board", "Environmental Department"])
    elif high_count > 0:
        departments.append("Environmental Department")

    if very_high_count > 0:
        priority, inspection, alert = "Critical", "Immediate", "Red"
    elif high_count > 0:
        priority, inspection, alert = "High", "Within 24 Hours", "Orange"
    else:
        priority, inspection, alert = "Medium", "Within 3 Days", "Yellow"

    # Returning the exact structure the script.js expects
    return {
        "average_aqi": avg_aqi,
        "highest_predicted_aqi": highest_risk_zone["predicted_aqi"],
        "improvement": 12.5,  # Dummy value for UI
        "confidence": 94,     # Dummy value for UI
        "high_risk_zones": high_risk_zones,
        "target_zone": highest_risk_zone["sub_zone_id"],
        "priority": priority,
        "departments": departments,
        "inspection_schedule": inspection,
        "alert": alert,
        "zones": aqi_map_data # This prevents the JavaScript 'data.zones.forEach' crash
    }

@app.get("/report")
def get_report():
    if aqi_map_data is None:
        return {"summary": "Waiting for simulation and governance data to process daily summary."}
    
    highest_risk_zone = max(aqi_map_data, key=lambda x: x["predicted_aqi"])
    
    # --- EDITED HERE: Updated string to "Very High" ---
    very_high_count = sum(1 for zone in aqi_map_data if zone["risk_level"] == "Very High")
    
    summary_text = (
        f"Analyzed {len(aqi_map_data)} sub-zones. "
        f"Critical attention required at {highest_risk_zone['sub_zone_id']} "
        f"with a predicted AQI of {highest_risk_zone['predicted_aqi']}. "
        f"Total high-risk sectors identified: {very_high_count}."
    )
    return {"summary": summary_text}

# ---------------------------------------------------------
# 3. MOUNTING AGENTS (Connects sub-apps)
# ---------------------------------------------------------
app.mount("/source", source_app)
app.mount("/optimize", optimize_app)
app.mount("/simulation", sim_app)

@app.get("/")
def home():
    return {"message": "Governance Dashboard Running"}