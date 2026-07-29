USE DATABASE DERMCLIMATE;
USE SCHEMA PUBLIC;

INSERT INTO papers (

    filename,
    title,
    authors,
    journal,
    publication_year,
    doi,
    pmcid,
    source_url

)

SELECT

    filename,
    title,

    PARSE_JSON(authors) AS authors,

    journal,
    publication_year,

    doi,
    pmcid,

    source_url

FROM (

    SELECT

        *,

        ROW_NUMBER() OVER (

            PARTITION BY
                COALESCE(
                    NULLIF(doi, ''),
                    NULLIF(pmcid, ''),
                    filename
                )

            ORDER BY
                CASE
                    WHEN filename LIKE '%(1)%' THEN 1
                    ELSE 0
                END,
                filename

        ) AS row_num

    FROM metadata_staging

    WHERE
        filename IS NOT NULL
        AND title IS NOT NULL

)

WHERE row_num = 1;