from enum import Enum
from dataclasses import dataclass
from app.models.risk_assessment import RiskAssessment
from app.models.retrieved_document import RetrievedDocument


class AnalysisStatus(Enum):
    SUCCESS = "success"
    NEEDS_INPUT = "needs_input"

@dataclass
class AnalysisResult:
    status: AnalysisStatus
    message: str

    response: str | None = None

    risk_assessment: RiskAssessment | None = None

    documents: list[RetrievedDocument] | None = None

    required_input: str | None = None