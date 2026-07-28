import requests

from app.metadata.metadata_enricher import MetadataEnricher
from app.metadata.paper_metadata import PaperMetadata


class CrossrefMetadataEnricher(MetadataEnricher):

    def __init__(self):
        self.base_url = "https://api.crossref.org/works"

    def enrich(self, metadata: PaperMetadata, text: str,) -> PaperMetadata:

        if metadata.doi is None:
            return metadata

        url = f"{self.base_url}/{metadata.doi}"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                return metadata

            data = response.json()
            message = data["message"]

            title = message.get("title", [None])[0]
            journal = message.get("container-title", [None])[0]

            authors = []

            for author in message.get("author", []):

                given = author.get("given", "")
                family = author.get("family", "")

                full_name = f"{given} {family}".strip()

                if full_name:
                    authors.append(full_name)

        except requests.RequestException:
            return metadata

        return PaperMetadata(
            filename=metadata.filename,
            title=title,
            authors=authors,
            journal=journal,
            publication_year=metadata.publication_year,
            doi=metadata.doi,
            pmcid=metadata.pmcid,
            source_url=metadata.source_url,
        )