from app.models.retrieved_document import RetrievedDocument
from app.retrieval.bm25_knowledge_retriever import BM25KnowledgeRetriever
from app.retrieval.faiss_knowledge_retriever import FAISSKnowledgeRetriever
from app.retrieval.knowledge_retriever import KnowledgeRetriever


class HybridKnowledgeRetriever(KnowledgeRetriever):
    def __init__(
        self,
        faiss_retriever: FAISSKnowledgeRetriever,
        bm25_retriever: BM25KnowledgeRetriever,
    ):
        self.faiss_retriever = faiss_retriever
        self.bm25_retriever = bm25_retriever

    def retrieve(self, query: str) -> list[RetrievedDocument]:
        semantic_results = self.faiss_retriever.retrieve(query)
        keyword_results = self.bm25_retriever.retrieve(query)

        combined_results = {}

        for document in semantic_results:
            combined_results[document.chunk_text] = document

        for document in keyword_results:
            combined_results[document.chunk_text] = document

        return list(combined_results.values())