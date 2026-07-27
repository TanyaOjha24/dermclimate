import faiss
import numpy as np

from app.models.knowledge_chunk import KnowledgeChunk

class FAISSIndexBuilder:
    def build( self, knowledge_chunks: list[KnowledgeChunk],):

        embeddings = []
        for knowledge_chunk in knowledge_chunks:
            embeddings.append(knowledge_chunk.embedding)

        embeddings = np.array(embeddings)
        embeddings = embeddings.astype(np.float32)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        return index