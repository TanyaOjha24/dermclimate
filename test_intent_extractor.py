from app.ai.cohere_llm import CohereLLM
from app.ai.intent_extractor import IntentExtractor
from app.config import COHERE_API_KEY, COHERE_MODEL

llm = CohereLLM(COHERE_API_KEY, COHERE_MODEL)
intent_extractor = IntentExtractor(llm)
user_message = "Should I use niacinamide today?"
parsed_request = intent_extractor.extract(user_message)
print(parsed_request)