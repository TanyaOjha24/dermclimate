from dataclasses import dataclass
from app.models.parsed_request import ParsedRequest

@dataclass
class ConversationState:
    pending_request: ParsedRequest | None = None
