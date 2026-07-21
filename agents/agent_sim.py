from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import requests

app = FastAPI()

# --- Pydantic Models (Corrected Formatting) ---

class OptimizationContext(BaseModel):
    zone_id: str
    is_anomaly_detected: bool

class SimulationInputs(BaseModel):
    traffic_light_adjustment_seconds: int
    suggested_flow_rate: float
    priority_level: str

class AnalyticalMetrics(BaseModel):
    predicted_pm_reduction_percent: float
    congestion_index: float

class SimulationInstructions(BaseModel):
    run_mode: str
    duration_cycles: int

class SubZoneData(BaseModel):
    sub_zone_id: str
    lat: float
    lng: float
    baseline_aqi: int

class SimulationPayload(BaseModel):
    request_id: str
    optimization_context: OptimizationContext
    simulation_inputs: SimulationInputs
    analytical_metrics: AnalyticalMetrics
    simulation_instructions: SimulationInstructions
    sub_zones: List[SubZoneData]

# --- Core Simulation Endpoint ---

@app.post("/simulation/run")
def run_simulation(payload: SimulationPayload):
    # Process the data
    sub_zones_list = payload.sub_zones
    total_reduction_pct = payload.analytical_metrics.predicted_pm_reduction_percent
    
    predicted_aqi_map_grid = []
    for zone in sub_zones_list:
        pred_aqi = int(zone.baseline_aqi * (1 - (total_reduction_pct / 100)))
        risk = "Very Poor" if pred_aqi > 200 else "Poor" if pred_aqi > 150 else "Moderate"
        
        predicted_aqi_map_grid.append({
            "sub_zone_id": zone.sub_zone_id,
            "lat": zone.lat,
            "lng": zone.lng,
            "baseline_aqi": zone.baseline_aqi,
            "predicted_aqi": pred_aqi,
            "risk_level": risk
        })
    
    # Forward data to the main Dashboard (Port 8000)
    try:
        requests.post("http://127.0.0.1:8000/aqi_agent", json=predicted_aqi_map_grid, timeout=5)
    except Exception as e:
        print(f"❌ Failed to forward to Dashboard: {e}")
        
    return {"status": "success", "request_id": payload.request_id}