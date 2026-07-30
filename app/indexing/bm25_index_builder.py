from rank_bm25 import BM25Okapi

from app.models.knowledge_chunk import KnowledgeChunk


class BM25IndexBuilder:
    def build(self, knowledge_chunks: list[KnowledgeChunk]):
        processed_chunks = [
            chunk.chunk_text.lower().split()
            for chunk in knowledge_chunks
        ]

        bm25 = BM25Okapi(processed_chunks)

        return bm25