import uuid
from app.embedding.embedding_model import EmbeddingModel
from app.models.knowledge_chunk import KnowledgeChunk
from app.indexing.chunker import Chunker


class KnowledgeChunkBuilder:

    def __init__(self, chunker: Chunker, embedding_model: EmbeddingModel,):
        self.chunker = chunker
        self.embedding_model = embedding_model

    def build( self, paper_title: str, source_url: str, text: str,
        ) -> list[KnowledgeChunk]:
        
        chunks = self.chunker.chunk(text)
        embeddings = self.embedding_model.embed(chunks)

        knowledge_chunks = []

        for chunk_number, (chunk_text, embedding) in enumerate(
            zip(chunks, embeddings),
            start=1,
        ):
            knowledge_chunk = KnowledgeChunk(
                id=str(uuid.uuid4()),
                paper_title=paper_title,
                source_url=source_url,
                chunk_number=chunk_number,
                chunk_text=chunk_text,
                embedding=embedding.tolist(),
            )

            knowledge_chunks.append(knowledge_chunk)

        return knowledge_chunks