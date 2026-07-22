from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List

from database.connection import get_db
from models.models import Zone, AQIData, WeatherData, SimulationHistory, Report
from models.data_schemas import ZoneSchema, AQIDataSchema, WeatherDataSchema, SimulationHistorySchema, ReportSchema, CombinedDataSchema

router = APIRouter(prefix="/data", tags=["data"])

@router.get("/zones", response_model=List[ZoneSchema])
async def get_zones(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Zone))
    zones = result.scalars().all()
    return zones

@router.get("/aqi/{zone_id}/current", response_model=AQIDataSchema)
async def get_current_aqi(zone_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AQIData)
        .where(AQIData.zone_id == zone_id)
        .order_by(desc(AQIData.timestamp))
        .limit(1)
    )
    aqi_data = result.scalars().first()
    if not aqi_data:
        raise HTTPException(status_code=404, detail="AQI data not found for this zone")
    return aqi_data

@router.get("/weather/{zone_id}/current", response_model=WeatherDataSchema)
async def get_current_weather(zone_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WeatherData)
        .where(WeatherData.zone_id == zone_id)
        .order_by(desc(WeatherData.timestamp))
        .limit(1)
    )
    weather_data = result.scalars().first()
    if not weather_data:
        raise HTTPException(status_code=404, detail="Weather data not found for this zone")
    return weather_data

@router.get("/combined/{zone_id}/current", response_model=CombinedDataSchema)
async def get_combined_current(zone_id: int, db: AsyncSession = Depends(get_db)):
    aqi = await get_current_aqi(zone_id, db)
    weather = await get_current_weather(zone_id, db)
    return CombinedDataSchema(aqi_data=aqi, weather_data=weather)

@router.get("/aqi/{zone_id}/history", response_model=List[AQIDataSchema])
async def get_aqi_history(zone_id: int, limit: int = 24, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AQIData)
        .where(AQIData.zone_id == zone_id)
        .order_by(desc(AQIData.timestamp))
        .limit(limit)
    )
    history = result.scalars().all()
    return history

@router.get("/history", response_model=List[SimulationHistorySchema])
async def get_simulation_history(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SimulationHistory).order_by(desc(SimulationHistory.timestamp)))
    return result.scalars().all()

@router.get("/reports", response_model=List[ReportSchema])
async def get_reports(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Report).order_by(desc(Report.generated_at)))
    return result.scalars().all()
