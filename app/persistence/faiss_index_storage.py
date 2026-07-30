from pathlib import Path

import faiss


class FAISSIndexStorage:

    def __init__(self, index_path: Path):
        self.index_path = index_path

    def save(self, index):
        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            index,
            str(self.index_path),
        )

    def load(self):
        return faiss.read_index(
            str(self.index_path),
        )

    def exists(self) -> bool:
        return self.index_path.exists()