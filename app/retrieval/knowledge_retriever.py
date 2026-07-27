from abc import ABC, abstractmethod
from app.models.retrieved_document import RetrievedDocument

class KnowledgeRetriever(ABC):

    @abstractmethod
    def retrieve(self, query: str) -> list[RetrievedDocument]:
        pass