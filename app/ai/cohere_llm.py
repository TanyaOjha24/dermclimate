from app.ai.llm import LLM
import cohere

class CohereLLM(LLM):
    def __init__( self, api_key: str, model: str,):
        self.model = model
        self.client = cohere.ClientV2(api_key=api_key)

    def generate(self, system_prompt: str, user_prompt: str, ) -> str:

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

        response = self.client.chat(
            model=self.model,
            messages=messages,
        )

        text = response.message.content[0].text

        # Cohere-specific cleanup
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        return text