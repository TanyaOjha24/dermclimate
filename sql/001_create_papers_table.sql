CREATE OR REPLACE TABLE papers (
    paper_id NUMBER AUTOINCREMENT PRIMARY KEY,

    filename STRING NOT NULL,
    title STRING NOT NULL,

    authors ARRAY,

    journal STRING,
    publication_year STRING,

    doi STRING,
    pmcid STRING,

    source_url STRING
);