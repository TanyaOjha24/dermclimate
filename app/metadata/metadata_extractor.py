from app.metadata.paper_metadata import PaperMetadata
import re

IGNORED_HEADERS = {
    "REVIEW ARTICLE",
    "ORIGINAL ARTICLE",
    "CASE REPORT",
    "EDITORIAL",
    "LETTER TO THE EDITOR",
}

DOI_PATTERN= re.compile(r'10\.\d{4,9}/[^\s]+')

PMCID_PATTERN = re.compile(r"PMC\d+")

AUTHOR_STOP_WORDS = {
    "ABSTRACT",
    "INTRODUCTION",
    "DOI",
    "PMCID",
}

YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")

URL_PATTERN = re.compile(r"https?://\S+")

AFFILIATION_KEYWORDS = {
    "DEPARTMENT",
    "UNIVERSITY",
    "COLLEGE",
    "HOSPITAL",
    "INSTITUTE",
    "FACULTY",
    "SCHOOL",
    "LABORATORY",
}


class MetadataExtractor:

    def extract(self, filename: str, text: str) -> PaperMetadata:
        title = self._extract_title(text)
        doi = self._extract_doi(text)
        pmcid = self._extract_pmcid(text)
        authors = self._extract_authors(text)
        publication_year  = self._extract_publication_year(text)
        source_url = self._extract_source_url(text)
        journal = self._extract_journal(text)

        metadata=  PaperMetadata(
            filename=filename,
            title=title,
            authors=authors,
            journal=journal,
            publication_year=publication_year,
            doi=doi,
            pmcid=pmcid,
            source_url=source_url,
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
        match = DOI_PATTERN.search(text)
        if match:
            return match.group()
        return None

    def _extract_pmcid(self, text: str) -> str | None:
        match = PMCID_PATTERN.search(text)

        if match:
            return match.group()

        return None


    def _extract_authors(self, text: str) -> list[str] | None:
        lines = [line.strip() for line in text.splitlines()]
        title = self._extract_title(text)
        if title is None:
            return None

        title_index = lines.index(title)
        authors = []
        for line in lines[title_index + 1:]:

            if not line:
                continue

            if line.upper() in AUTHOR_STOP_WORDS:
                break

            if DOI_PATTERN.search(line):
                break

            if PMCID_PATTERN.search(line):
                break

            authors.append(line)

        if authors:
            return authors

        return None

    
    def _extract_publication_year(self, text: str) -> str | None:
        match = YEAR_PATTERN.search(text)
        if match:
            return match.group()
        return None

    def _extract_source_url(self, text: str) -> str | None:
        match = URL_PATTERN.search(text)
        if match:
            return match.group()
        return None


    def _extract_journal(self, text: str) -> str | None:
        lines = [line.strip() for line in text.splitlines()]
        title = self._extract_title(text)
        if title is None:
            return None

        authors = self._extract_authors(text)
        title_index = lines.index(title)
        for line in lines[title_index + 1:]:

            if not line:
                continue

            if line.upper() in AUTHOR_STOP_WORDS:
                break

            if DOI_PATTERN.search(line):
                break

            if PMCID_PATTERN.search(line):
                break

            if any(keyword in line.upper() for keyword in AFFILIATION_KEYWORDS):
                continue

            if authors and line in authors:
                continue

            return line

        return None