import asyncio
import random
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import Zone, AQIData, WeatherData
from database.connection import SessionLocal

CHENNAI_ZONES = [
    {"name": "Adyar", "lat": 13.0012, "lon": 80.2565, "desc": "Residential and commercial neighborhood"},
    {"name": "Anna Nagar", "lat": 13.0850, "lon": 80.2101, "desc": "Planned residential area"},
    {"name": "Ambattur", "lat": 13.1143, "lon": 80.1548, "desc": "Industrial and IT hub"},
    {"name": "Alandur", "lat": 12.9975, "lon": 80.2006, "desc": "Near Chennai Airport"},
    {"name": "Guindy", "lat": 13.0067, "lon": 80.2206, "desc": "Industrial estate and national park"},
    {"name": "Kodambakkam", "lat": 13.0528, "lon": 80.2255, "desc": "Commercial center"},
    {"name": "Mylapore", "lat": 13.0368, "lon": 80.2676, "desc": "Cultural and residential hub"},
    {"name": "Perungudi", "lat": 12.9654, "lon": 80.2461, "desc": "IT corridor"},
    {"name": "Tambaram", "lat": 12.9249, "lon": 80.1000, "desc": "Southern suburb"},
    {"name": "T Nagar", "lat": 13.0418, "lon": 80.2341, "desc": "Major shopping district"},
    {"name": "Velachery", "lat": 12.9815, "lon": 80.2180, "desc": "Residential and commercial hub"},
    {"name": "Sholinganallur", "lat": 12.9010, "lon": 80.2279, "desc": "IT SEZ on OMR"},
    {"name": "Royapuram", "lat": 13.1137, "lon": 80.2954, "desc": "Northern neighborhood"},
    {"name": "Madhavaram", "lat": 13.1486, "lon": 80.2306, "desc": "Northern suburb"},
    {"name": "Porur", "lat": 13.0382, "lon": 80.1565, "desc": "Western suburb, IT hub"}
]

async def seed_data():
    async with SessionLocal() as db:
        result = await db.execute(select(Zone))
        existing_zones = result.scalars().all()
        
        if existing_zones:
            print("Zones already seeded.")
            return

        print("Seeding zones...")
        db_zones = []
        for z in CHENNAI_ZONES:
            zone = Zone(
                name=z["name"],
                latitude=z["lat"],
                longitude=z["lon"],
                description=z["desc"]
            )
            db.add(zone)
            db_zones.append(zone)
        
        await db.commit()
        
        result = await db.execute(select(Zone))
        db_zones = result.scalars().all()
        
        print("Seeding initial mock AQI and Weather data...")
        now = datetime.utcnow()
        for zone in db_zones:
            for i in range(24):
                timestamp = now - timedelta(hours=i)
                base_aqi = random.uniform(50, 150)
                if zone.name in ["Ambattur", "Guindy"]:
                    base_aqi += random.uniform(20, 50)
                    
                aqi_data = AQIData(
                    zone_id=zone.id,
                    timestamp=timestamp,
                    aqi=base_aqi,
                    pm25=base_aqi * 0.4 + random.uniform(-10, 10),
                    pm10=base_aqi * 0.7 + random.uniform(-15, 15),
                    no2=random.uniform(10, 60),
                    so2=random.uniform(5, 30),
                    co=random.uniform(0.5, 2.5),
                    o3=random.uniform(20, 80)
                )
                weather_data = WeatherData(
                    zone_id=zone.id,
                    timestamp=timestamp,
                    temperature=random.uniform(28, 35),
                    humidity=random.uniform(60, 90),
                    pressure=1010 + random.uniform(-5, 5),
                    wind_speed=random.uniform(5, 15),
                    visibility=random.uniform(5, 10),
                    rain=random.uniform(0, 5) if random.random() > 0.8 else 0
                )
                db.add(aqi_data)
                db.add(weather_data)
        
        await db.commit()
        print("Database seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_data())
