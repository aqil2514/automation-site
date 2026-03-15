from newspaper import Article, Config
from playwright.async_api import async_playwright

from src.schemas.article import ArticleSchema


# async def get_article(url: str) -> ArticleSchema:
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()

#         try:
#             # 1. Blokir Gambar agar cepat & hemat RAM
#             await page.route(
#                 "**/*.{png,jpg,jpeg,webp,gif}", lambda route: route.abort()
#             )

#             # 2. Buka URL
#             await page.goto(url, wait_until="networkidle", timeout=30000)

#             # 3. Hapus elemen pengganggu (Cookie Banners) sebelum parsing
#             await page.evaluate("""() => {
#                 const selectors = ['[id*="cookie"]', '[class*="cookie"]', '[id*="policy"]', '.modal', '.overlay'];
#                 selectors.forEach(s => {
#                     document.querySelectorAll(s).forEach(el => el.remove());
#                 });
#             }""")

#             html_content = await page.content()

#             article = Article(url)
#             article.set_html(html_content)
#             article.parse()

#             return ArticleSchema(
#                 title=article.title,
#                 content=article.text,
#                 url=url,
#                 authors=article.authors,
#                 top_image=article.top_image,
#             )
#         finally:
#             await browser.close()


async def get_article(url: str) -> ArticleSchema:
    async with async_playwright() as p:
        # Gunakan Chrome asli jika terinstall agar tidak mudah terdeteksi bot
        browser = await p.chromium.launch(headless=True)
        # Tambahkan User-Agent manusia asli
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            # 1. BLOKIR RESOURCE BERAT (Supaya cepet & gak kena timeout)
            await page.route(
                "**/*.{png,jpg,jpeg,webp,gif,css,woff,woff2,svg}",
                lambda route: route.abort(),
            )

            # 2. NAVIGASI (Gunakan domcontentloaded, JANGAN networkidle)
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)

            # 3. TUNGGU ELEMEN UTAMA (Opsional tapi membantu content kosong)
            # Biasanya artikel berita ada di tag <article> atau <p>
            try:
                await page.wait_for_selector("p", timeout=5000)
            except:  # noqa: E722
                pass  # Lanjut aja kalau gak ketemu

            html_content = await page.content()

            # 4. PARSING DENGAN NEWSPAPER
            config = Config()
            config.request_timeout = 10

            article = Article(url, config=config)
            article.set_html(html_content)
            article.parse()

            # Kalau content masih kosong, jangan masukkan ke list
            status = "success" if len(article.text) > 100 else "failed"

            return ArticleSchema(
                title=article.title,
                content=article.text,
                url=url,
                authors=article.authors,
                top_image=article.top_image,
                status=status,
            )
        except Exception as e:
            return ArticleSchema(title="Error", content="", url=url, status="failed")
        finally:
            await browser.close()
