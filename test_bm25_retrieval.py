from app.embedding.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)

from app.indexing.bm25_index_builder import BM25IndexBuilder
from app.indexing.faiss_index_builder import FAISSIndexBuilder

from app.persistence.snowflake_knowledge_base_storage import (
    SnowflakeKnowledgeBaseStorage,
)

from app.rag.knowledge_base_service import KnowledgeBaseService


embedding_model = SentenceTransformerEmbeddingModel()

storage = SnowflakeKnowledgeBaseStorage()

faiss_index_builder = FAISSIndexBuilder()


knowledge_base_service = KnowledgeBaseService(
    knowledge_chunk_builder=None,
    storage=storage,
    faiss_index_builder=faiss_index_builder,
    embedding_model=embedding_model,
    bm25_index_builder=BM25IndexBuilder(),
)


retriever = knowledge_base_service.create_bm25_retriever()

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