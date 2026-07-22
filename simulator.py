import json
from openai import AsyncOpenAI
from config.settings import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def simulate_impact(current_data: dict, selected_interventions: list) -> dict:
    if not settings.OPENAI_API_KEY:
        reduction_factor = sum(int(i.get('expected_aqi_reduction', 0)) for i in selected_interventions)
        new_aqi = max(20, current_data.get('aqi', 100) - reduction_factor)
        improvement = round(((current_data.get('aqi', 100) - new_aqi) / current_data.get('aqi', 100)) * 100, 2)
        
        return {
            "future_aqi": new_aqi,
            "pollutant_reductions": {
                "pm25": f"-{improvement}%",
                "pm10": f"-{improvement}%",
                "no2": f"-{improvement * 0.8}%"
            },
            "health_benefits": "Reduced risk of respiratory issues by estimated 10%.",
            "carbon_reduction": f"Estimated {improvement * 50} tons/year",
            "improvement_percentage": improvement,
            "confidence_interval": "+/- 5 AQI points"
        }

    prompt = f"""
    Current Environmental Data:
    {json.dumps(current_data)}
    
    Selected Interventions:
    {json.dumps(selected_interventions)}
    
    Simulate the combined impact of these interventions on the current data.
    Respond STRICTLY in JSON format:
    {{
        "future_aqi": 80,
        "pollutant_reductions": {{"pm25": "-15%", "no2": "-20%"}},
        "health_benefits": "Description",
        "carbon_reduction": "Estimated tons",
        "improvement_percentage": 25.5,
        "confidence_interval": "+/- 10 points"
    }}
    """
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"AI Simulator Error: {e}")
        return {"error": "Simulation failed"}
