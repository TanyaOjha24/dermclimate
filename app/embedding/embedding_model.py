from abc import ABC, abstractmethod


class EmbeddingModel(ABC):

    @abstractmethod
    def embed(self, text):
        pass

    @abstractmethod
    def dimension(self):
        pass