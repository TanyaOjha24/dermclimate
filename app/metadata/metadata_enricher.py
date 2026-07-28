from abc import ABC, abstractmethod

from app.metadata.paper_metadata import PaperMetadata


class MetadataEnricher(ABC):

    @abstractmethod
    def enrich(
        self,
        metadata: PaperMetadata,
        text: str,
    ) -> PaperMetadata:
        pass