from src.db.connection import get_pool
from .sql import INSERT_ARTICLE_POSTING
from .model import ArticlePosting


async def insert_article_posting(payload: ArticlePosting) -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                INSERT_ARTICLE_POSTING,
                payload.article_id,
                payload.platform_name,
                payload.status,
                payload.notes,
            )
        except Exception as e:
            print(f"Error insert_article_posting: {e}")
            raise e
