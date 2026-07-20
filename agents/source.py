from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import json

app = FastAPI(title="Source Intelligence Agent")

# 1. Input model to receive data from the user/gateway
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

class SourceIntelligenceAgent:
    def __init__(self, data: InputData):
        self.data = data

    def source_attribution(self):
        traffic = round(self.data.traffic_index * 0.5, 1)
        industry = round(self.data.industrial_emission_index * 0.4, 1)
        construction = 15 if self.data.dust_detected else 5
        waste = 8 if self.data.smoke_detected else 3
        residential = 6
        sources = [
            {"source": "Traffic", "contribution_percent": traffic},
            {"source": "Industrial Emissions", "contribution_percent": industry},
            {"source": "Construction Dust", "contribution_percent": construction},
            {"source": "Waste Burning", "contribution_percent": waste},
            {"source": "Residential Biomass", "contribution_percent": residential}
        ]
        dominant = max(sources, key=lambda x: x["contribution_percent"])
        return dominant, sources

    def hotspot_prediction(self):
        predicted_aqi = self.data.aqi + (self.data.traffic_index + self.data.industrial_emission_index) // 10
        hotspots = [
            {"location": "Industrial Corridor", "predicted_aqi": predicted_aqi + 20, "risk_level": "Very High"},
            {"location": "City Center", "predicted_aqi": predicted_aqi, "risk_level": "High"},
            {"location": "Construction Zone", "predicted_aqi": predicted_aqi - 10, "risk_level": "Medium"}
        ]
        highest = max(hotspots, key=lambda x: x["predicted_aqi"])
        return highest, hotspots

    def risk_score(self):
        score = min(100, int(self.data.aqi * 0.3 + self.data.traffic_index * 0.3 + self.data.industrial_emission_index * 0.4))
        level = "Critical" if score >= 85 else "High" if score >= 70 else "Medium" if score >= 50 else "Low"
        return score, level

    def generate_report(self):
        dominant, sources = self.source_attribution()
        highest_hotspot, hotspots = self.hotspot_prediction()
        score, level = self.risk_score()
        return {
            "agent_name": "Source Intelligence AI Agent",
            "city": self.data.city_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_air_quality": {"aqi": self.data.aqi},
            "source_attribution": {"dominant_source": dominant["source"], "source_contributions": sources},
            "hotspot_prediction": {"highest_risk_hotspot": highest_hotspot, "all_hotspots": hotspots},
            "compliance_risk": {"risk_score": score, "risk_level": level}
        }

@app.post("/process")
def process_data(data: InputData):
    agent = SourceIntelligenceAgent(data)
    return agent.generate_report()