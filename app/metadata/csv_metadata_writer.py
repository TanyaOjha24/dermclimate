import csv
import os
from app.metadata.paper_metadata import PaperMetadata
from dataclasses import fields

class CSVMetadataWriter:

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def append(self, metadata: PaperMetadata):
            file_exists = os.path.exists(self.csv_path)
            with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames = [field.name for field in fields(PaperMetadata)])
                if not file_exists:
                    writer.writeheader()
                writer.writerow(metadata.__dict__)

    