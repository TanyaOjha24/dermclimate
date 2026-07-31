from pathlib import Path

from app.embedding.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)

from app.indexing.faiss_index_builder import FAISSIndexBuilder
from app.indexing.bm25_index_builder import BM25IndexBuilder

from app.persistence.faiss_index_storage import FAISSIndexStorage
from app.persistence.bm25_index_storage import BM25IndexStorage

from app.persistence.snowflake_knowledge_base_storage import (
    SnowflakeKnowledgeBaseStorage,
)

from app.rag.knowledge_base_service import KnowledgeBaseService

from app.retrieval.hybrid_knowledge_retriever import (
    HybridKnowledgeRetriever,
)

from app.reranking.cross_encoder_reranker import (
    CrossEncoderReranker,
)

# -------------------------------------------------
# Project Paths
# -------------------------------------------------

project_root = Path(__file__).parent

faiss_index_storage = FAISSIndexStorage(
    project_root / "indexes" / "faiss.index"
)

bm25_index_storage = BM25IndexStorage(
    project_root / "indexes" / "bm25.pkl"
)

# -------------------------------------------------
# Services
# -------------------------------------------------

embedding_model = SentenceTransformerEmbeddingModel()

storage = SnowflakeKnowledgeBaseStorage()

faiss_index_builder = FAISSIndexBuilder()

bm25_index_builder = BM25IndexBuilder()

knowledge_base_service = KnowledgeBaseService(
    knowledge_chunk_builder=None,
    storage=storage,
    faiss_index_builder=faiss_index_builder,
    bm25_index_builder=bm25_index_builder,
    faiss_index_storage=faiss_index_storage,
    bm25_index_storage=bm25_index_storage,
    embedding_model=embedding_model,
)

# -------------------------------------------------
# Create Retrievers
# -------------------------------------------------

faiss_retriever = knowledge_base_service.create_faiss_retriever()

bm25_retriever = knowledge_base_service.create_bm25_retriever()

hybrid_retriever = HybridKnowledgeRetriever(
    faiss_retriever=faiss_retriever,
    bm25_retriever=bm25_retriever,
)

# -------------------------------------------------
# Create Reranker
# -------------------------------------------------

reranker = CrossEncoderReranker()

# -------------------------------------------------
# Test
# -------------------------------------------------

query = "How does low humidity affect the skin barrier?"

candidate_documents = hybrid_retriever.retrieve(query)

results = reranker.rerank(
    query=query,
    documents=candidate_documents,
    top_k=5,
)


print(f"\nQuery: {query}\n")

for i, document in enumerate(results, start=1):
    print("=" * 80)
    print(f"Result {i}")
    print(f"Paper : {document.paper_title}")
    print(f"Score : {document.score}")
    print(f"Source: {document.source_url}")
    print()
    print(document.chunk_text)
    print()