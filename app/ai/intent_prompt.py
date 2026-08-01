from app.ai.prompt_builder import PromptBuilder


class IntentPrompt(PromptBuilder):

    def build(self, user_message: str,) -> tuple[str, str]:

        system_prompt = """
            You are an intent extraction assistant for DermClimate.

            Extract the following fields from the user's message:

            - intent
            - product
            - ingredients
            - concern
            - city

            Return ONLY a valid JSON object.

            Do not use markdown.
            Do not explain your reasoning.
            Do not include any text before or after the JSON.
            Do not wrap the JSON in ```json```.

            If a field is missing, use null.

            Example:

            {
            "intent": "analyze_product",
            "product": "CeraVe Moisturizing Cream",
            "ingredients": null,
            "concern": null,
            "city": "Boston"
            }
            """.strip()

        return (
            system_prompt,
            user_message,
        )