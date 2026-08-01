from app.models.analysis_result import (
    AnalysisResult,
    AnalysisStatus,
)
from app.models.parsed_request import ParsedRequest


class ProductAnalysisService:

    def __init__(
        self,
        climate_fetcher,
        feature_engineer,
        risk_engine,
        ingredient_fetcher,
        retriever,
        reranker,
        prompt,
        llm,
    ):
        self.climate_fetcher = climate_fetcher
        self.feature_engineer = feature_engineer
        self.risk_engine = risk_engine
        self.ingredient_fetcher = ingredient_fetcher
        self.retriever = retriever
        self.reranker = reranker
        self.prompt = prompt
        self.llm = llm


    def analyze(self, request: ParsedRequest):
        validation_result = self.validate(request)

        if validation_result is not None:
            return validation_result

        # Climate Pipeline
        weather = self.climate_fetcher.get_weather(request.city)
        engineered_weather = self.feature_engineer(weather)
        risk_assessment = self.risk_engine.score(engineered_weather)

        # Ingredient Pipeline
        ingredients = request.ingredients
        if request.product:
            ingredients = self.ingredient_fetcher.get_product_ingredients(
                request.product,
            )

        # Retrieval Pipeline
        retrieval_query = request.product or ingredients
        retrieved_documents = self.retriever.retrieve(retrieval_query,)

        reranked_documents = self.reranker.rerank(
            query=retrieval_query,
            documents=retrieved_documents,
        )

        system_prompt, user_prompt = self.prompt.build(
            request=request,
            ingredients=ingredients,
            risk_assessment=risk_assessment,
            documents=reranked_documents,
        )

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
        return AnalysisResult(
            status=AnalysisStatus.SUCCESS,
            message="Analysis completed successfully.",
            response=response,
            risk_assessment=risk_assessment,
            documents=reranked_documents,
        )



    def validate(self, request: ParsedRequest) -> AnalysisResult | None:

        if not request.product and not request.ingredients:
            return AnalysisResult(
                status=AnalysisStatus.NEEDS_INPUT,
                message="Which product or ingredient would you like to analyze?",
                required_input="product",
            )

        if not request.city:
            return AnalysisResult(
                status=AnalysisStatus.NEEDS_INPUT,
                message="Which city are you in?",
                required_input="city",
            )

        return None