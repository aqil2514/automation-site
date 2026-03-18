from src.db.connection import get_pool

from .sql import SELECT_APPROVED_ARTICLE
from .model import ProcessedArticles


async def select_approved_article() -> ProcessedArticles | None:
    pool = await get_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(SELECT_APPROVED_ARTICLE)

        if not row:
            print("Tidak ada artikel terbaru yang akan dipublish")
            return None

        print(row)

        data = dict(row)

        try:
            return ProcessedArticles(**data)
        except Exception as e:
            print(f"Error validasi data artikel: {e}")
            return None
