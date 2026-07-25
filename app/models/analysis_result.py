from enum import Enum
from dataclasses import dataclass


class AnalysisStatus(Enum):
    SUCCESS = "success"
    NEEDS_INPUT = "needs_input"

@dataclass
class AnalysisResult:
    status: AnalysisStatus
    message: str
    required_input: str | None = None