from abc import ABC, abstractmethod

from app.models.retrieved_document import RetrievedDocument


class Reranker(ABC):

    @abstractmethod
    def rerank(
        self,
        query: str,
        documents: list[RetrievedDocument],
        top_k: int = 5,
    ) -> list[RetrievedDocument]:
        pass