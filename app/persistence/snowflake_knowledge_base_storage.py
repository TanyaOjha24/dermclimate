import json

from app.models.knowledge_chunk import KnowledgeChunk
from app.persistence.knowledge_base_storage import KnowledgeBaseStorage
from app.persistence.snowflake_connector import get_snowflake_connection

class SnowflakeKnowledgeBaseStorage(KnowledgeBaseStorage):
    def save( self, knowledge_chunks: list[KnowledgeChunk],) -> None:

        conn = get_snowflake_connection()
        cursor = conn.cursor()

        for knowledge_chunk in knowledge_chunks:

            cursor.execute(
                """
                INSERT INTO knowledge_chunks (
                    id,
                    paper_title,
                    source_url,
                    chunk_number,
                    chunk_text,
                    embedding
                )
                SELECT
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    PARSE_JSON(%s)
                """,
                (
                    knowledge_chunk.id,
                    knowledge_chunk.paper_title,
                    knowledge_chunk.source_url,
                    knowledge_chunk.chunk_number,
                    knowledge_chunk.chunk_text,
                    json.dumps(knowledge_chunk.embedding),
                ),
            )

        conn.commit()

        cursor.close()
        conn.close()


    def load( self,) -> list[KnowledgeChunk]:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                id,
                paper_title,
                source_url,
                chunk_number,
                chunk_text,
                embedding
            FROM knowledge_chunks
            """
        )

        rows = cursor.fetchall()
        knowledge_chunks = []
        for row in rows:
            knowledge_chunk = KnowledgeChunk(
                id=row[0],
                paper_title=row[1],
                source_url=row[2],
                chunk_number=row[3],
                chunk_text=row[4],
                embedding=json.loads(row[5]),
            )
            knowledge_chunks.append(knowledge_chunk)

        cursor.close()
        conn.close()

        return knowledge_chunks
