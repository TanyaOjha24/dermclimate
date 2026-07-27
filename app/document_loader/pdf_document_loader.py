from pypdf import PdfReader
from app.document_loader.document_loader import DocumentLoader


class PDFDocumentLoader(DocumentLoader):

    def load( self,file_path: str,) -> str:
        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            
            if page_text:
                text += page_text + "\n"

        return text