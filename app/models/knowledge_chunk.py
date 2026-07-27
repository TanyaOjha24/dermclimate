from dataclasses import dataclass


@dataclass
class KnowledgeChunk:
    id: str
    paper_title: str
    source_url: str
    chunk_number: int
    chunk_text: str
    embedding: list[float]