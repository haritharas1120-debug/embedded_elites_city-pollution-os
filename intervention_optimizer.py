import json
from openai import AsyncOpenAI
from config.settings import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def optimize_interventions(source_analysis: dict, zone_name: str) -> list:
    if not settings.OPENAI_API_KEY:
        return [
            {
                "id": "traffic_restriction",
                "name": "Heavy Vehicle Restriction",
                "priority": "High",
                "expected_aqi_reduction": 15,
                "estimated_cost": "$5,000",
                "implementation_difficulty": "Medium",
                "time_required": "1 week",
                "confidence": 90,
                "description": "Restrict heavy commercial vehicles during peak hours."
            },
            {
                "id": "dust_suppression",
                "name": "Construction Dust Suppression",
                "priority": "Medium",
                "expected_aqi_reduction": 8,
                "estimated_cost": "$2,000",
                "implementation_difficulty": "Low",
                "time_required": "Immediate",
                "confidence": 85,
                "description": "Mandate water sprinkling at major construction sites."
            }
        ]

    prompt = f"""
    Based on the following pollution source analysis for '{zone_name}':
    {json.dumps(source_analysis)}
    
    Recommend 2-4 specific interventions to reduce air pollution.
    Respond STRICTLY in JSON format as a list of dictionaries with this structure:
    {{
        "interventions": [
            {{
                "id": "unique_string_id",
                "name": "Intervention Name",
                "priority": "High/Medium/Low",
                "expected_aqi_reduction": 10,
                "estimated_cost": "$10,000",
                "implementation_difficulty": "High/Medium/Low",
                "time_required": "1 month",
                "confidence": 80,
                "description": "Brief explanation"
            }}
        ]
    }}
    """
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content).get("interventions", [])
    except Exception as e:
        print(f"AI Optimizer Error: {e}")
        return []
