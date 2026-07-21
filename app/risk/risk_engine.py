from abc import ABC, abstractmethod

class RiskEngine(ABC):

    @abstractmethod
    def score(self, features):
        pass

    @abstractmethod
    def version(self):
        pass