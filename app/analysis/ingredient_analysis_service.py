from app.models.analysis_result import (
    AnalysisResult,
    AnalysisStatus,
)
from app.models.parsed_request import ParsedRequest


class IngredientAnalysisService:

    def __init__(
        self,
        retriever,
        reranker,
        prompt,
        llm,
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.prompt = prompt
        self.llm = llm

    def analyze(
        self,
        request: ParsedRequest,
    ):

        validation_result = self.validate(
            request,
        )

        if validation_result is not None:
            return validation_result

        ingredients = request.ingredients

        retrieval_query = ", ".join(
            ingredients,
        )

        retrieved_documents = self.retriever.retrieve(
            retrieval_query,
        )

        reranked_documents = self.reranker.rerank(
            query=retrieval_query,
            documents=retrieved_documents,
        )

        system_prompt, user_prompt = self.prompt.build(
            request=request,
            ingredients=ingredients,
            documents=reranked_documents,
        )

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return AnalysisResult(
            status=AnalysisStatus.SUCCESS,
            message="Ingredient analysis completed successfully.",
            response=response,
            documents=reranked_documents,
        )

    def validate(
        self,
        request: ParsedRequest,
    ) -> AnalysisResult | None:

        if not request.ingredients:
            return AnalysisResult(
                status=AnalysisStatus.NEEDS_INPUT,
                message="Which ingredient would you like to analyze?",
                required_input="ingredients",
            )

        return None