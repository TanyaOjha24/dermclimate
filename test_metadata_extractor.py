from pathlib import Path
from app.document_loader.pdf_document_loader import PDFDocumentLoader
from app.metadata.metadata_extractor import MetadataExtractor

project_root = Path(__file__).parent

paper_path = project_root / "papers" / "484_2026_Article_3145.pdf"

loader = PDFDocumentLoader()
text = loader.load(str(paper_path))
lines = text.splitlines()

for i, line in enumerate(lines[:100]):
    if line.strip():
        print(f"{i}: {line}")
        
extractor = MetadataExtractor()

metadata = extractor.extract(
    filename=paper_path.name,
    text=text,
)

print(metadata)