import json
from openai import AsyncOpenAI
from config.settings import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def analyze_sources(aqi_data: dict, zone_name: str) -> dict:
    if not settings.OPENAI_API_KEY:
        # Mock response if no API key
        return {
            "sources": [
                {"name": "Traffic", "contribution": 45},
                {"name": "Industrial", "contribution": 30},
                {"name": "Construction", "contribution": 15},
                {"name": "Biomass Burning", "contribution": 5},
                {"name": "Dust", "contribution": 5}
            ],
            "confidence_score": 85,
            "reasoning": f"Based on high NO2 and PM2.5 levels in {zone_name}, traffic is the primary contributor."
        }

    prompt = f"""
    Analyze the following live environmental data for the zone '{zone_name}' in Chennai:
    {json.dumps(aqi_data)}
    
    Determine the primary pollution sources and their estimated contribution percentages.
    Consider standard urban pollution factors (Traffic, Industrial, Construction, Biomass Burning, Dust).
    
    Respond STRICTLY in JSON format with the following structure:
    {{
        "sources": [
            {{"name": "SourceName", "contribution": 10}}
        ],
        "confidence_score": 85,
        "reasoning": "Brief explanation of the analysis based on the specific pollutant levels."
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
        print(f"AI Analysis Error: {e}")
        return {"error": "Failed to analyze sources"}
