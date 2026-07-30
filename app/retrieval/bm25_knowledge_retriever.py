import numpy as np

from app.models.knowledge_chunk import KnowledgeChunk
from app.models.retrieved_document import RetrievedDocument
from app.retrieval.knowledge_retriever import KnowledgeRetriever


class BM25KnowledgeRetriever(KnowledgeRetriever):

    def __init__(self, bm25_index, knowledge_chunks: list[KnowledgeChunk], k: int = 3,):
        self.bm25_index = bm25_index
        self.knowledge_chunks = knowledge_chunks
        self.k = k

    def retrieve(self, query: str) -> list[RetrievedDocument]:

        query_tokens = query.lower().split()

        scores = self.bm25_index.get_scores(query_tokens)

        top_indices = np.argsort(scores)[::-1][: self.k]

        retrieved_documents = []

        for index in top_indices:

            if scores[index] <= 0:
                continue

            knowledge_chunk = self.knowledge_chunks[index]

            retrieved_documents.append(
                RetrievedDocument(
                    chunk_text=knowledge_chunk.chunk_text,
                    paper_title=knowledge_chunk.paper_title,
                    source_url=knowledge_chunk.source_url,
                    score=float(scores[index]),
                )
            )

        return retrieved_documents