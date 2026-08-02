from app.ai.prompt_builder import PromptBuilder
from app.models.parsed_request import ParsedRequest
from app.models.retrieved_document import RetrievedDocument


class IngredientAnalysisPrompt(PromptBuilder):

    def build(
        self,
        request: ParsedRequest,
        ingredients: list[str],
        documents: list[RetrievedDocument],
    ) -> tuple[str, str]:

        system_prompt = """
You are DermClimate, an evidence-based skincare ingredient analysis assistant.

Your job is to explain skincare ingredients using only the provided scientific evidence.

Guidelines:
- Base your analysis on the retrieved dermatology literature.
- Do not invent scientific claims.
- Clearly explain ingredient functions.
- Mention limitations when evidence is limited.
- Keep the explanation understandable for a general user.
""".strip()

        ingredient_text = ", ".join(ingredients)

        evidence = "\n\n".join(
            f"Title: {doc.paper_title}\n"
            f"{doc.chunk_text}"
            for doc in documents
        )

        user_prompt = f"""
Ingredients:

{ingredient_text}

Scientific Evidence:

{evidence}

Please provide:

1. Primary function of each ingredient.
2. Evidence-based benefits.
3. Possible drawbacks or irritation risks.
4. Which skin types benefit most.
5. Overall scientific summary.
""".strip()

        return (
            system_prompt,
            user_prompt,
        )