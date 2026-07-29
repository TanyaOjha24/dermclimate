USE DATABASE DERMCLIMATE;
USE SCHEMA PUBLIC;

SELECT COUNT(*)
FROM knowledge_chunks
WHERE paper_id IS NULL;

SELECT paper_id, COUNT(*)
FROM knowledge_chunks
GROUP BY paper_id
ORDER BY COUNT(*) DESC;

SELECT
    kc.paper_id,
    p.title,
    COUNT(*) AS chunk_count
FROM knowledge_chunks kc
JOIN papers p
    ON kc.paper_id = p.paper_id
GROUP BY kc.paper_id, p.title
ORDER BY chunk_count DESC;

SELECT COUNT(*)
FROM knowledge_chunks kc
LEFT JOIN papers p
    ON kc.paper_title = p.title
WHERE p.paper_id IS NULL;