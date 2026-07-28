from app.metadata.crossref_metadata_enricher import CrossrefMetadataEnricher
from app.metadata.paper_metadata import PaperMetadata


metadata = PaperMetadata(
    filename="484_2026_Article_3145.pdf",
    title=None,
    authors=None,
    journal=None,
    publication_year="2026",
    doi="10.1007/s00484-026-03145-0",
    pmcid=None,
    source_url=None,
)

enricher = CrossrefMetadataEnricher()

enriched_metadata = enricher.enrich(
    metadata=metadata,
    text="",
)

print("\nReturned metadata:")
print(enriched_metadata)


from pathlib import Path
from app.metadata.csv_metadata_writer import CSVMetadataWriter

project_root = Path(__file__).parent

metadata_dir = project_root / "metadata"
metadata_dir.mkdir(exist_ok=True)

csv_path = metadata_dir / "paper_metadata.csv"

writer = CSVMetadataWriter(str(csv_path))

writer.append(enriched_metadata)

print("\nMetadata written successfully!")