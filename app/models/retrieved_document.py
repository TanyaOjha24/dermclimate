from dataclasses import dataclass


@dataclass
class RetrievedDocument:
    chunk_text: str
    paper_title: str
    source_url: str
    score: float