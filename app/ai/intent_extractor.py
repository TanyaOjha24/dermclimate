import json
from app.models.parsed_request import ParsedRequest

class IntentExtractor:
    def __init__(self, llm):
        self.llm = llm

    def extract(self, user_message: str):
        system_prompt = (
            "You are an intent extraction assistant for DermClimate. "
            "Your task is to analyze the user's message and identify "
            "their intent, product name, ingredients, and skin concern "
            "if they are mentioned. "
            "Return a JSON object with the fields: "
            "intent, product, ingredients, concern. "
            "Use null if a field is not present."
        )
        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_message,
        )

        parsed_response = json.loads(response)

        return ParsedRequest(
            intent=parsed_response.get("intent"),
            product=parsed_response.get("product"),
            ingredients=parsed_response.get("ingredients"),
            concern=parsed_response.get("concern"),
        )