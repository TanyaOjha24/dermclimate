from pathlib import Path
from app.document_loader.pdf_document_loader import PDFDocumentLoader

from app.embedding.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)

from app.indexing.knowledge_chunk_builder import KnowledgeChunkBuilder
from app.indexing.recursive_chunker import RecursiveChunker

from app.persistence.snowflake_knowledge_base_storage import (
    SnowflakeKnowledgeBaseStorage,
)

from app.indexing.faiss_index_builder import FAISSIndexBuilder
from app.rag.knowledge_base_service import KnowledgeBaseService


loader = PDFDocumentLoader()

project_root = Path(__file__).parent.parent

paper_path = project_root / "papers" / "484_2026_Article_3145.pdf"

text = loader.load(str(paper_path))

chunker = RecursiveChunker()

embedding_model = SentenceTransformerEmbeddingModel()

knowledge_chunk_builder = KnowledgeChunkBuilder(
    chunker=chunker,
    embedding_model=embedding_model,
)

storage = SnowflakeKnowledgeBaseStorage()

faiss_index_builder = FAISSIndexBuilder()

knowledge_base_service = KnowledgeBaseService(
    knowledge_chunk_builder=knowledge_chunk_builder,
    storage=storage,
    faiss_index_builder=faiss_index_builder,
    embedding_model=embedding_model,
)

knowledge_base_service.ingest_paper(
    paper_title="YOUR PAPER TITLE",
    source_url="YOUR PAPER URL",
    text=text,
)

print("Paper ingested successfully!")