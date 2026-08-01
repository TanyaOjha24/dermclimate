import json
from app.models.parsed_request import ParsedRequest
from app.ai.prompt_builder import PromptBuilder
from app.ai.llm import LLM


class IntentExtractor:

    def __init__(self, llm: LLM,prompt: PromptBuilder):
        self.llm = llm
        self.prompt = prompt

    def extract(self, user_message: str,) -> ParsedRequest:

        system_prompt, user_prompt = self.prompt.build(
            user_message,
        )

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        parsed_response = json.loads(response)

        return ParsedRequest(
            intent=parsed_response.get("intent"),
            product=parsed_response.get("product"),
            ingredients=parsed_response.get("ingredients"),
            concern=parsed_response.get("concern"),
            city=parsed_response.get("city")
        )