USE DATABASE DERMCLIMATE;
USE SCHEMA PUBLIC;

ALTER TABLE knowledge_chunks
ADD COLUMN paper_id NUMBER;

SELECT COUNT(*)
FROM knowledge_chunks kc
LEFT JOIN papers p
    ON kc.paper_title = p.title
WHERE p.paper_id IS NULL;