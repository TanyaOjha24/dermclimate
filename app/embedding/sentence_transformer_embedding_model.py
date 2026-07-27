from sentence_transformers import SentenceTransformer

from app.embedding.embedding_model import EmbeddingModel

class SentenceTransformerEmbeddingModel(EmbeddingModel):

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text):
        return self.model.encode(text)
    
    def dimension(self):
        return self.model.get_embedding_dimension()