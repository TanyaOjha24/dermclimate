from abc import ABC, abstractmethod
from app.models.knowledge_chunk import KnowledgeChunk

class KnowledgeBaseStorage(ABC):

    @abstractmethod
    def save( self, knowledge_chunks: list[KnowledgeChunk],):
        pass

    @abstractmethod
    def load(self) -> list[KnowledgeChunk]:
        pass