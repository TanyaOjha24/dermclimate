from app.metadata.paper_metadata import PaperMetadata
import re

IGNORED_HEADERS = {
    "REVIEW ARTICLE",
    "ORIGINAL ARTICLE",
    "CASE REPORT",
    "EDITORIAL",
    "LETTER TO THE EDITOR",
}

doi_pattern = re.compile(r'10\.\d{4,9}/[^\s]+')
PMCID_PATTERN = re.compile(r"PMC\d+")


class MetadataExtractor:

    def extract(self, filename: str, text: str) -> PaperMetadata:
        title = self._extract_title(text)
        doi = self._extract_doi(text)
        pmcid = self._extract_pmcid(text)

        metadata=  PaperMetadata(
            filename=filename,
            title=title,
            authors=None,
            journal=None,
            publication_year=None,
            doi=doi,
            pmcid=pmcid,
            source_url=None,
            topic=None,
            ingredient_group=None,
            evidence_level=None,
        )

        return metadata
    

    def _extract_title(self, text: str) -> str | None:
        lines = text.splitlines()
        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line.upper() in IGNORED_HEADERS:
                continue

            return line

        return None


    def _extract_doi(self, text: str) -> str | None:
        match = doi_pattern.search(text)
        if match:
            return match.group()
        return None

    def _extract_pmcid(self, text: str) -> str | None:
        match = PMCID_PATTERN.search(text)

        if match:
            return match.group()

        return None
