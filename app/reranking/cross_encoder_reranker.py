from sentence_transformers import CrossEncoder

from app.models.retrieved_document import RetrievedDocument
from app.reranking.reranker import Reranker


class CrossEncoderReranker(Reranker):

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )


    def rerank(self, query: str, documents: list[RetrievedDocument], top_k: int = 5,) -> list[RetrievedDocument]:

        if not documents:
            return []

        pairs = [
            (query, document.chunk_text)
            for document in documents
        ]

        scores = self.model.predict(pairs)

        ranked_documents = list(
            zip(
                documents,
                scores,
            )
        )

        ranked_documents.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        return [
            document
            for document, score in ranked_documents[:top_k]
        ]