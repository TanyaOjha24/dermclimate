from pathlib import Path
import pickle


class BM25IndexStorage:

    def __init__(self, index_path: Path):
        self.index_path = index_path

    def save(self, index):

        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(self.index_path, "wb") as file:
            pickle.dump(index, file)

    def load(self):

        with open(self.index_path, "rb") as file:
            return pickle.load(file)

    def exists(self) -> bool:
        return self.index_path.exists()