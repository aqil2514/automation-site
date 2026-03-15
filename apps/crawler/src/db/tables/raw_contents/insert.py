from typing import List
from src.db.connection import get_pool
from src.db.tables.raw_contents.model import RawContent
from src.db.tables.raw_contents.sql import INSERT_NEW_RAW_CONTENTS


async def insert_new_raw_contents(payload: List[RawContent]) -> None:
    pool = await get_pool()

    async with pool.acquire() as conn:
        try:
            data_tuples = [
                (
                    p.source_url,
                    p.title,
                    p.content_raw,
                    p.image_url,
                    p.status,
                )
                for p in payload
            ]

            await conn.executemany(INSERT_NEW_RAW_CONTENTS, data_tuples)

            print(f"✅ Berhasil memasukkan {len(payload)} data ke database.")

        except Exception as e:
            print(f"Terjadi kesalahan saat upload data raws: {e}")
            raise e
