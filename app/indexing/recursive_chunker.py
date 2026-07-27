from app.indexing.chunker import Chunker
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RecursiveChunker(Chunker):
    def __init__(self, chunk_size : int=500, chunk_overlap: int=100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str) -> list[str]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

        return text_splitter.split_text(text)
