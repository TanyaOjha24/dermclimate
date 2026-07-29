USE DATABASE DERMCLIMATE;
USE SCHEMA PUBLIC;

UPDATE knowledge_chunks AS kc
SET paper_id = p.paper_id
FROM papers AS p
WHERE kc.paper_title = p.title;
