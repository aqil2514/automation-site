from playwright.async_api import async_playwright
from playwright_stealth import Stealth

from src.crawlers.kompasiana import start_kompasiana
from src.db.tables.processed_articles.model import ProcessedArticles


async def write_article(article: ProcessedArticles | None) -> None:
    if not article:
        return None

    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await start_kompasiana(page, article)
