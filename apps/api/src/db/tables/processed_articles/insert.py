import uuid

from src.db.connection import get_pool
from .sql import INSERT_PROCESSED_ARTICLE
from .model import ProcessedArticle


async def insert_processed_article(payload: ProcessedArticle) -> uuid.UUID:
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            # Mengembalikan ID yang baru dibuat
            article_id = await conn.fetchval(
                INSERT_PROCESSED_ARTICLE,
                payload.id,
                payload.raw_content_id,
                payload.title,
                payload.slug,
                payload.content_full,
                payload.excerpt,
                payload.tags,
                payload.image_url,
                payload.status,
            )
            return article_id
        except Exception as e:
            print(f"Error insert_processed_article: {e}")
            raise e
