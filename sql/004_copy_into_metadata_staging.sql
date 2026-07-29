USE DATABASE DERMCLIMATE;
USE SCHEMA PUBLIC;

COPY INTO metadata_staging
FROM @metadata_stage/paper_metadata.csv.gz
FILE_FORMAT = (
    TYPE = CSV
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
);