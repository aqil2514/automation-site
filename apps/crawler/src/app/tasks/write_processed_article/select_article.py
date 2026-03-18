from src.db.tables.processed_articles.model import ProcessedArticles
from src.db.tables.processed_articles.select_approved import select_approved_article


async def search_article() -> ProcessedArticles | None:
    print("Mencari data artikel yang sudah diapproved...")
    article = await select_approved_article()
    if not article:
        return None
    print(f"Artikel yang diapproved ditemukan.\n Judul '{article.title}'")

    return article
