import asyncio

from .select_article import search_article
from .write_article import write_article

# TEST : python -m src.app.tasks.write_processed_article.__init__


async def write_processed_article():
    article = await search_article()
    await write_article(article)


if __name__ == "__main__":
    asyncio.run(write_processed_article())
