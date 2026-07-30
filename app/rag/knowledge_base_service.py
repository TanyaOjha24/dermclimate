from app.embedding.embedding_model import EmbeddingModel
from app.indexing.faiss_index_builder import FAISSIndexBuilder
from app.indexing.knowledge_chunk_builder import KnowledgeChunkBuilder
from app.persistence.knowledge_base_storage import KnowledgeBaseStorage
from app.retrieval.faiss_knowledge_retriever import FAISSKnowledgeRetriever


class KnowledgeBaseService:
    def __init__(
    self,
    knowledge_chunk_builder: KnowledgeChunkBuilder,
    storage: KnowledgeBaseStorage,
    faiss_index_builder: FAISSIndexBuilder,
    embedding_model: EmbeddingModel,
    ):
        self.knowledge_chunk_builder = knowledge_chunk_builder
        self.storage = storage
        self.faiss_index_builder = faiss_index_builder
        self.embedding_model = embedding_model


    def ingest_paper(
    self,
    paper_title: str,
    source_url: str,
    text: str,
    )-> None:
        knowledge_chunks = self.knowledge_chunk_builder.build(
            paper_title=paper_title,
            source_url=source_url,
            text=text,
        )

        self.storage.save(knowledge_chunks)


    def create_faiss_retriever( self,)-> FAISSKnowledgeRetriever:
        knowledge_chunks = self.storage.load()
        faiss_index = self.faiss_index_builder.build(knowledge_chunks)
        retriever = FAISSKnowledgeRetriever(
            embedding_model=self.embedding_model,
            faiss_index=faiss_index,
            knowledge_chunks=knowledge_chunks,
        )

        return retriever