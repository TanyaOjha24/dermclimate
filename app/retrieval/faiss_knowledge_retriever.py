import numpy as np
from app.models.retrieved_document import RetrievedDocument
from app.retrieval.knowledge_retriever import KnowledgeRetriever
from app.models.knowledge_chunk import KnowledgeChunk


class FAISSKnowledgeRetriever(KnowledgeRetriever):

    def __init__(self,embedding_model,faiss_index,knowledge_chunks: list[KnowledgeChunk],k: int = 3,):
        self.embedding_model = embedding_model
        self.faiss_index = faiss_index
        self.knowledge_chunks = knowledge_chunks
        self.k = k

    def retrieve(self, query: str) -> list[RetrievedDocument]:
        query_embedding = self.embedding_model.embed(query)

        # FAISS expects a float32 2D NumPy array
        query_embedding = query_embedding.astype(np.float32)
        query_embedding = query_embedding.reshape(1, -1)

        distances, indices = self.faiss_index.search(
            query_embedding,
            self.k,
        )

        retrieved_documents = []

        for score, index in zip(distances[0], indices[0]):
            # FAISS returns -1 if no valid neighbor is found
            if index == -1:
                continue

            knowledge_chunk = self.knowledge_chunks[index]

            retrieved_documents.append(
                RetrievedDocument(
                    chunk_text=knowledge_chunk.chunk_text,
                    paper_title=knowledge_chunk.paper_title,
                    source_url=knowledge_chunk.source_url,
                    score=float(score),
                )
            )

        return retrieved_documents