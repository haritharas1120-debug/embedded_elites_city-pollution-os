from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Intervention Optimization Agent", description="Member 2: Recommends best actions to reduce pollution.")

# --- INPUT MODELS (Based on your exact JSON file) ---
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

# Main Input Request matching your JSON
class TeamOptimizationRequest(BaseModel):
    request_id: str
    optimization_context: OptimizationContext
    simulation_inputs: SimulationInputs
    analytical_metrics: AnalyticalMetrics
    simulation_instructions: SimulationInstructions

# --- OUTPUT MODEL ---
class TeamOptimizationResponse(BaseModel):
    request_id: str
    zone_id: str
    action_taken: str
    final_traffic_adjustment: int
    status: str

@app.post("/optimize", response_model=TeamOptimizationResponse)
def run_team_optimization(data: TeamOptimizationRequest):
    # Optimization Logic
    action = "Monitor only, normal flow"
    final_adjustment = data.simulation_inputs.traffic_light_adjustment_seconds
    
    # Logic based on metrics
    if data.optimization_context.is_anomaly_detected:
        if data.analytical_metrics.congestion_index > 0.75:
            action = "CRITICAL: Heavy congestion. Maximizing green light!"
            final_adjustment += 15  
        else:
            action = "WARNING: Adjust traffic flow to reduce PM levels"
            
    return TeamOptimizationResponse(
        request_id=data.request_id,
        zone_id=data.optimization_context.zone_id,
        action_taken=action,
        final_traffic_adjustment=final_adjustment,
        status="Optimization Completed & Sent to Simulation"
    )
