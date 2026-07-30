from app.embedding.embedding_model import EmbeddingModel
from app.indexing.faiss_index_builder import FAISSIndexBuilder
from app.indexing.knowledge_chunk_builder import KnowledgeChunkBuilder
from app.persistence.faiss_index_storage import FAISSIndexStorage
from app.persistence.knowledge_base_storage import KnowledgeBaseStorage
from app.retrieval.faiss_knowledge_retriever import FAISSKnowledgeRetriever
from app.indexing.bm25_index_builder import BM25IndexBuilder
from app.retrieval.bm25_knowledge_retriever import BM25KnowledgeRetriever
from app.persistence.bm25_index_storage import BM25IndexStorage


class KnowledgeBaseService:
    def __init__(
    self,
    knowledge_chunk_builder: KnowledgeChunkBuilder,
    storage: KnowledgeBaseStorage,
    faiss_index_builder: FAISSIndexBuilder,
    bm25_index_builder: BM25IndexBuilder,
    faiss_index_storage: FAISSIndexStorage,
    bm25_index_storage: BM25IndexStorage,
    embedding_model: EmbeddingModel,
    ):
        self.knowledge_chunk_builder = knowledge_chunk_builder
        self.storage = storage
        self.faiss_index_builder = faiss_index_builder
        self.bm25_index_builder = bm25_index_builder
        self.embedding_model = embedding_model
        self.faiss_index_storage = faiss_index_storage
        self.bm25_index_storage = bm25_index_storage


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


    def create_faiss_retriever(self) -> FAISSKnowledgeRetriever:
        knowledge_chunks = self.storage.load()
        if self.faiss_index_storage.exists():
            print("Loading FAISS index from disk...")
            faiss_index = self.faiss_index_storage.load()

        else:
            print("Building FAISS index...")
            faiss_index = self.faiss_index_builder.build(
                knowledge_chunks
            )
            self.faiss_index_storage.save(
                faiss_index
            )

        retriever = FAISSKnowledgeRetriever(
            embedding_model=self.embedding_model,
            faiss_index=faiss_index,
            knowledge_chunks=knowledge_chunks,
        )

        return retriever


    def create_bm25_retriever(self) -> BM25KnowledgeRetriever:
        knowledge_chunks = self.storage.load()
        if self.bm25_index_storage.exists():
            print("Loading BM25 index from disk...")
            bm25_index = self.bm25_index_storage.load()

        else:
            print("Building BM25 index...")
            bm25_index = self.bm25_index_builder.build(
                knowledge_chunks
            )

            self.bm25_index_storage.save(
                bm25_index
            )

        retriever = BM25KnowledgeRetriever(
            bm25_index=bm25_index,
            knowledge_chunks=knowledge_chunks,
            k=3,
        )

        return retriever