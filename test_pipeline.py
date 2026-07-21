import requests
import json

# 1. Pipeline Simulation Data
pipeline_data = {
    "city_name": "Chennai",
    "aqi": 178,
    "temperature": 34.5,
    "humidity": 65.0,
    "wind_speed": 10.0,
    "wind_direction": "SW",
    "traffic_index": 85,
    "industrial_emission_index": 72,
    "dust_detected": True,
    "smoke_detected": True
}

# 2. Dashboard Map Data (This populates the frontend)

dashboard_data = [
    {
        "sub_zone_id": "Chennai-Central",
        "lat": 13.0827,
        "lng": 80.2707,
        "baseline_aqi": 345,   
        "predicted_aqi": 302,  
        "risk_level": "Very High"   # Changed from Very Poor
    },
    {
        "sub_zone_id": "Chennai-South",
        "lat": 12.9827,
        "lng": 80.2507,
        "baseline_aqi": 250,   
        "predicted_aqi": 218,  
        "risk_level": "High"        # Changed from Poor
    },
    {
        "sub_zone_id": "Chennai-Besant-Nagar",
        "lat": 13.0002,
        "lng": 80.2668,
        "baseline_aqi": 55,    
        "predicted_aqi": 42,    
        "risk_level": "Low"         # Low remains Low
    }
]

def run_test():
    try:
        # --- STEP 1: RUN PIPELINE ---
        print("🚀 [Step 1] Sending data to City Pollution OS Pipeline (/run-pipeline)...")
        pipeline_response = requests.post("http://127.0.0.1:8000/run-pipeline", json=pipeline_data, timeout=10)
        
        if pipeline_response.status_code == 200:
            print("✅ Pipeline Success!")
        else:
            print(f"❌ Pipeline Error: {pipeline_response.text}")
            return

        # --- STEP 2: SEND DATA TO DASHBOARD ---
        print("\n🚀 [Step 2] Sending mapped data to the Governance Dashboard (/aqi_agent)...")
        dashboard_response = requests.post("http://127.0.0.1:8000/aqi_agent", json=dashboard_data, timeout=10)
        
        if dashboard_response.status_code == 200:
            print("✅ Dashboard Data Sent Successfully!")
            print("🎉 You can now refresh your browser to see the data on the dashboard.")
        else:
            print(f"❌ Dashboard Error: {dashboard_response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the Server. (Is main.py running?)")
    except requests.exceptions.Timeout:
        print("❌ Error: The request timed out.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_test()