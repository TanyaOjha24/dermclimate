from pathlib import Path

from app.document_loader.pdf_document_loader import PDFDocumentLoader

from app.embedding.sentence_transformer_embedding_model import (
    SentenceTransformerEmbeddingModel,
)

from app.indexing.faiss_index_builder import FAISSIndexBuilder
from app.indexing.knowledge_chunk_builder import KnowledgeChunkBuilder
from app.indexing.recursive_chunker import RecursiveChunker

from app.metadata.crossref_metadata_enricher import CrossrefMetadataEnricher
from app.metadata.csv_metadata_writer import CSVMetadataWriter
from app.metadata.metadata_extractor import MetadataExtractor

from app.persistence.snowflake_knowledge_base_storage import (
    SnowflakeKnowledgeBaseStorage,
)

from app.rag.knowledge_base_service import KnowledgeBaseService


# ----------------------------
# Project paths
# ----------------------------

project_root = Path(__file__).parent.parent

papers_dir = project_root / "papers"

metadata_dir = project_root / "metadata"
metadata_dir.mkdir(exist_ok=True)

csv_path = metadata_dir / "paper_metadata.csv"


# ----------------------------
# Services
# ----------------------------

loader = PDFDocumentLoader()

metadata_extractor = MetadataExtractor()

metadata_enricher = CrossrefMetadataEnricher()

csv_writer = CSVMetadataWriter(str(csv_path))

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


# ----------------------------
# Ingest Papers
# ----------------------------

for paper_path in papers_dir.glob("*.pdf"):

    print(f"\nIngesting {paper_path.name}...")

    text = loader.load(str(paper_path))

    metadata = metadata_extractor.extract(
        filename=paper_path.name,
        text=text,
    )

    metadata = metadata_enricher.enrich(
        metadata=metadata,
        text=text,
    )

    csv_writer.append(metadata)

    knowledge_base_service.ingest_paper(
        paper_title=metadata.title,
        source_url=metadata.source_url,
        text=text,
    )

    print(f"Finished ingesting {paper_path.name}")

print("\nAll papers ingested successfully!")