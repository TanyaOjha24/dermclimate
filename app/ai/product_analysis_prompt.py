from app.ai.prompt_builder import PromptBuilder
from app.models.parsed_request import ParsedRequest
from app.models.risk_assessment import RiskAssessment
from app.models.retrieved_document import RetrievedDocument


class ProductAnalysisPrompt(PromptBuilder):

    def build(
        self,
        request: ParsedRequest,
        ingredients: list[str],
        risk_assessment: RiskAssessment,
        documents: list[RetrievedDocument],
    ) -> tuple[str, str]:

        system_prompt = """
You are DermClimate, an evidence-based skincare analysis assistant.

Your job is to evaluate skincare products using:
- the product ingredients,
- the user's climate conditions,
- the calculated skin barrier risk,
- the provided dermatology literature.

Guidelines:
- Base your analysis primarily on the retrieved scientific evidence.
- Do not invent scientific claims.
- If evidence is limited, explicitly mention it.
- Explain your reasoning clearly.
- Keep the response understandable for a general user.
- If ingredients are unsuitable for the current climate, explain why.
- If ingredients support the skin barrier, explain how.
""".strip()

        ingredient_text = ", ".join(ingredients)

        evidence = "\n\n".join(
            f"Title: {doc.paper_title}\n"
            f"{doc.chunk_text}"
            for doc in documents
        )

        user_prompt = f"""
User Request:
Analyze {request.product or "the provided ingredients"}.

Ingredients:
{ingredient_text}

Climate Risk:
Score: {risk_assessment.score}
Version: {risk_assessment.version}

Scientific Evidence:
{evidence}

Please provide:

1. Overall suitability of this product for today's climate.
2. Ingredient analysis.
3. How the climate affects the product's performance.
4. Evidence-based explanation.
5. Practical skincare recommendation.
""".strip()

        return (
            system_prompt,
            user_prompt,
        )