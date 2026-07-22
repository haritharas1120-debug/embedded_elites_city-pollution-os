from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List, Dict, Any

from database.connection import get_db
from models.models import Zone, AQIData
from agents.source_intelligence import analyze_sources
from agents.intervention_optimizer import optimize_interventions
from agents.simulator import simulate_impact

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/analyze/{zone_id}")
async def analyze_zone(zone_id: int, db: AsyncSession = Depends(get_db)):
    # 1. Fetch data
    zone_result = await db.execute(select(Zone).where(Zone.id == zone_id))
    zone = zone_result.scalars().first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")

    aqi_result = await db.execute(
        select(AQIData)
        .where(AQIData.zone_id == zone_id)
        .order_by(desc(AQIData.timestamp))
        .limit(1)
    )
    aqi_data = aqi_result.scalars().first()
    if not aqi_data:
        raise HTTPException(status_code=404, detail="No AQI data available for analysis")

    # Convert to dict for AI
    data_dict = {
        "aqi": aqi_data.aqi,
        "pm25": aqi_data.pm25,
        "pm10": aqi_data.pm10,
        "no2": aqi_data.no2,
        "so2": aqi_data.so2,
        "co": aqi_data.co,
        "temperature": aqi_data.temperature,
        "wind_speed": aqi_data.wind_speed,
    }

    # 2. Source Intelligence
    source_analysis = await analyze_sources(data_dict, zone.name)
    
    # 3. Intervention Optimization
    interventions = await optimize_interventions(source_analysis, zone.name)
    
    return {
        "zone": zone.name,
        "current_data": data_dict,
        "source_analysis": source_analysis,
        "recommended_interventions": interventions
    }

@router.post("/simulate")
async def run_simulation(payload: Dict[str, Any]):
    # Expects current_data and selected_interventions in payload
    current_data = payload.get("current_data", {})
    selected_interventions = payload.get("selected_interventions", [])
    
    if not current_data or not selected_interventions:
        raise HTTPException(status_code=400, detail="Missing data for simulation")
        
    simulation_result = await simulate_impact(current_data, selected_interventions)
    return simulation_result
