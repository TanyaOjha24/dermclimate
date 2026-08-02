from app.models.analysis_result import (
    AnalysisResult,
    AnalysisStatus,
)
from app.models.parsed_request import ParsedRequest


class ClimateAnalysisService:

    def __init__(
        self,
        climate_fetcher,
        feature_engineer,
        risk_engine,
        prompt,
        llm,
    ):
        self.climate_fetcher = climate_fetcher
        self.feature_engineer = feature_engineer
        self.risk_engine = risk_engine
        self.prompt = prompt
        self.llm = llm


    def validate(
        self,
        request: ParsedRequest,
    ) -> AnalysisResult | None:

        if not request.city:
            return AnalysisResult(
                status=AnalysisStatus.NEEDS_INPUT,
                message="Which city are you in?",
                required_input="city",
            )

        return None


    def analyze(
        self,
        request: ParsedRequest,
    ):

        validation_result = self.validate(
            request,
        )

        if validation_result is not None:
            return validation_result

        weather = self.climate_fetcher.get_weather(
            request.city,
        )

        engineered_weather = self.feature_engineer(
            weather,
        )

        risk_assessment = self.risk_engine.score(
            engineered_weather,
        )

        system_prompt, user_prompt = self.prompt.build(
            request=request,
            weather=engineered_weather,
            risk_assessment=risk_assessment,
        )

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return AnalysisResult(
            status=AnalysisStatus.SUCCESS,
            message="Climate analysis completed successfully.",
            response=response,
            risk_assessment=risk_assessment,
        )