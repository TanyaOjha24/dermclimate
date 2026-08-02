import json

from app.ai.llm import LLM
from app.ai.prompt_builder import PromptBuilder
from app.models.parsed_request import ParsedRequest


INTENT_MAP = {
    "product_analysis": "product_analysis",
    "analyze_product": "product_analysis",

    "ingredient_analysis": "ingredient_analysis",
    "analyze_ingredient": "ingredient_analysis",

    "weather_query": "weather_query",
    "weather_analysis": "weather_query",
    "climate_analysis": "weather_query",

    "routine_recommendation": "routine_recommendation",
    "routine_analysis": "routine_recommendation",
}


class IntentExtractor:

    def __init__(
        self,
        llm: LLM,
        prompt: PromptBuilder,
    ):
        self.llm = llm
        self.prompt = prompt

    def extract(
        self,
        user_message: str,
    ) -> ParsedRequest:

        system_prompt, user_prompt = self.prompt.build(
            user_message,
        )

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        ##########
        print("\nLLM RESPONSE:")
        print(response)
        print()########

        parsed_response = json.loads(response)

        intent = parsed_response.get("intent")

        normalized_intent = INTENT_MAP.get(
            intent,
            intent,
        )

        return ParsedRequest(
            intent=normalized_intent,
            product=parsed_response.get("product"),
            ingredients=parsed_response.get("ingredients"),
            concern=parsed_response.get("concern"),
            city=parsed_response.get("city"),
        )