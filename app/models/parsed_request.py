"""
Represents the structured interpretation of a user's message.

The IntentExtractor converts the LLM's JSON response into a ParsedRequest,
which is then passed to downstream services for routing and analysis.
"""

from dataclasses import dataclass

@dataclass
class ParsedRequest:
    intent: str | None = None
    product: str | None = None
    ingredients: list[str] | None = None
    concern: str | None = None
    city: str | None = None