from pathlib import Path

from app.embedding.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)

from app.indexing.faiss_index_builder import FAISSIndexBuilder
from app.indexing.bm25_index_builder import BM25IndexBuilder

from app.persistence.faiss_index_storage import FAISSIndexStorage

from app.persistence.snowflake_knowledge_base_storage import (
    SnowflakeKnowledgeBaseStorage,
)

from app.rag.knowledge_base_service import KnowledgeBaseService


# ----------------------------
# Project paths
# ----------------------------

project_root = Path(__file__).parent

faiss_index_storage = FAISSIndexStorage(
    project_root / "indexes" / "faiss.index"
)


# ----------------------------
# Services
# ----------------------------

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
    embedding_model=embedding_model,
)


# ----------------------------
# Test
# ----------------------------

retriever = knowledge_base_service.create_faiss_retriever()

query = "How does low humidity affect the skin barrier?"

results = retriever.retrieve(query)

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