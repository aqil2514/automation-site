from src.db.connection import get_pool

from .sql import SELECT_RAW_CONTENTS, SELECT_RAW_CONTENTS_BY_STATUS
from .model import RawContent


async def select_raw_contents(status_filter: str | None = None) -> list[RawContent]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        if status_filter:
            # Jika ada filter status, gunakan query dengan WHERE
            rows = await conn.fetch(SELECT_RAW_CONTENTS_BY_STATUS, status_filter)
        else:
            # Jika tidak ada, ambil semua
            rows = await conn.fetch(SELECT_RAW_CONTENTS)

        return [RawContent.model_validate(dict(row)) for row in rows]
