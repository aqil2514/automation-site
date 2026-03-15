from newspaper import Article, Config
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

from src.schemas.article import ArticleSchema


async def get_article(url: str) -> ArticleSchema:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # 1. Blokir Gambar agar cepat & hemat RAM
            await page.route(
                "**/*.{png,jpg,jpeg,webp,gif}", lambda route: route.abort()
            )

            # 2. Buka URL
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # 3. Hapus elemen pengganggu (Cookie Banners) sebelum parsing
            await page.evaluate("""() => {
                const selectors = ['[id*="cookie"]', '[class*="cookie"]', '[id*="policy"]', '.modal', '.overlay'];
                selectors.forEach(s => {
                    document.querySelectorAll(s).forEach(el => el.remove());
                });
            }""")

            html_content = await page.content()

            article = Article(url)
            article.set_html(html_content)
            article.parse()

            return ArticleSchema(
                title=article.title,
                content=article.text,
                url=url,
                authors=article.authors,
                top_image=article.top_image,
            )
        finally:
            await browser.close()
