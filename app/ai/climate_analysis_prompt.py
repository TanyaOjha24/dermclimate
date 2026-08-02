from app.ai.prompt_builder import PromptBuilder
from app.models.parsed_request import ParsedRequest
from app.models.risk_assessment import RiskAssessment
from app.models.engineered_weather import EngineeredWeather


class ClimateAnalysisPrompt(PromptBuilder):

    def build(
        self,
        request: ParsedRequest,
        weather: EngineeredWeather,
        risk_assessment: RiskAssessment,
    ) -> tuple[str, str]:

        system_prompt = """
You are DermClimate, an evidence-based skin barrier assistant.

Your job is to explain how today's climate affects the user's skin.

Use:
- temperature
- humidity
- UV index
- wind
- calculated barrier risk

Do not invent weather conditions.
Explain your reasoning clearly.
Provide practical skincare recommendations.
""".strip()

        user_prompt = f"""
City:
{request.city}

Today's Climate:

Temperature: {weather.temperature}°C
Humidity: {weather.humidity}%
Wind Speed: {weather.wind_speed} km/h
UV Index: {weather.uv}

Engineered Weather:

Temperature Category: {weather.temp_category}
Humidity Category: {weather.humid_category}
Wind Category: {weather.wind_category}
UV Category: {weather.uv_category}

Barrier Risk:

Score: {risk_assessment.score}
Version: {risk_assessment.version}

Please provide:

1. Overall skin barrier risk.
2. Which weather factors contribute most.
3. What skin issues may occur today.
4. Practical skincare recommendations.
""".strip()

        return (
            system_prompt,
            user_prompt,
        )