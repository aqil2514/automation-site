from playwright.async_api import Page

from src.db.tables.processed_articles.model import ProcessedArticles

from .write import kompasiana_write

from .login import kompasiana_login


async def start_kompasiana(page: Page, processedArticle: ProcessedArticles) -> None:
    await kompasiana_login(page)
    await kompasiana_write(page, article=processedArticle)
