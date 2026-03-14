from src.db.connection import get_pool
from src.db.tables.raw_contents.model import RawContent
from src.db.tables.raw_contents.sql import INSERT_NEW_RAW_CONTENTS


async def insert_new_raw_contents(payload:RawContent)->None:
    pool = await get_pool()

    async with pool.acquire() as conn:
        try:
            await conn.execute(
                INSERT_NEW_RAW_CONTENTS,
                payload.source_url,
                payload.title,
                payload.content_raw,
                payload.image_url,
                payload.status   
            )
        except Exception as e:
            print("Terjadi kesalahan saat upload data raws insert_new_raw_contents")
            raise e