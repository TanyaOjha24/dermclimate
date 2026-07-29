USE DATABASE DERMCLIMATE;
USE SCHEMA PUBLIC;

CREATE OR REPLACE TABLE metadata_staging (

    filename STRING,
    title STRING,
    authors STRING,

    journal STRING,
    publication_year STRING,

    doi STRING,
    pmcid STRING,

    source_url STRING

);
