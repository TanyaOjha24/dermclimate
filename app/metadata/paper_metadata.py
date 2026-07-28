from dataclasses import dataclass


@dataclass
class PaperMetadata:
    filename: str
    title: str
    authors: str | None
    journal: str | None
    publication_year: str | None
    doi: str | None
    pmcid: str | None
    source_url: str | None
    topic: str | None
    ingredient_group: str | None
    evidence_level: str | None