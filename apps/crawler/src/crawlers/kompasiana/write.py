import asyncio

from playwright.async_api import Page

from src.services.download_image import download_image
from src.db.tables.processed_articles.model import ProcessedArticles


async def _select_category(page: Page) -> None:
    await page.locator("span").filter(has_text="Pilih Kategori").click()
    await page.locator("span").filter(has_text="Financial").click()


async def _fill_title(page: Page, title: str) -> None:
    await page.get_by_role("textbox", name="Judul").click()
    await page.get_by_role("textbox", name="Judul").fill(title)


async def _fill_content(page: Page, content: str, image_path: str | None) -> None:
    # 1. Pastikan editor utama sudah siap
    editor = page.locator(".fr-element")
    await editor.wait_for(state="visible", timeout=15000)

    if image_path:
        # 2. Proses Insert Image
        await page.get_by_role("button", name="Insert Image").click()
        await asyncio.sleep(1)

        # Selektor input file
        await page.set_input_files(
            "input[aria-labelledby^='fr-image-upload-layer']", image_path
        )

        # 3. Isi Caption
        caption_input = page.locator("span.image-desc-input")
        await caption_input.wait_for(state="visible", timeout=15000)
        await caption_input.fill("Test Caption ajah")

        # 4. Konfirmasi dan Pindah Fokus
        await caption_input.press("Enter")
        await asyncio.sleep(1)

        # Klik editor agar kursor keluar dari kotak gambar
        await editor.click(force=True)
        await asyncio.sleep(1)

    # 5. MENAMBAHKAN KONTEN (APPEND)
    # Menggunakan metodeinsertAdjacentHTML jauh lebih stabil untuk menambahkan elemen baru
    # tanpa merusak elemen gambar yang sudah ada (DOM nodes).
    await editor.evaluate(
        """(el, text) => {
            const p = document.createElement('p');
            p.innerText = text;
            el.appendChild(p);
        }""",
        content,
    )
    print("Gambar aman, teks berhasil ditambahkan di bawahnya.")


async def _select_recommended_article(page: Page) -> None:
    await page.get_by_role("button", name="Cari Konten").click()
    await page.locator(".dashboardPopup__option").first.click()
    await page.locator(
        "li:nth-child(2) > .dashboardPopup__label > .dashboardPopup__art > .dashboardPopup__option"
    ).first.click()
    await page.locator(
        "li:nth-child(3) > .dashboardPopup__label > .dashboardPopup__art > .dashboardPopup__option"
    ).first.click()
    await page.get_by_role("button", name="Gunakan Konten").click()


async def _fill_teaser_and_recommended_tag(
    page: Page, teaser: str, tags: list[str]
) -> None:
    await page.get_by_role("textbox", name="Tulis teaser untuk menarik").click()
    await page.get_by_role("textbox", name="Tulis teaser untuk menarik").fill(teaser)
    await page.get_by_text("REKOMENDASI", exact=True).click()
    await page.get_by_role("textbox", name="Tambahkan tag...").click()
    for tag in tags:
        await page.get_by_role("textbox", name="Tambahkan tag...").fill(tag)
        await page.get_by_role("textbox", name="Tambahkan tag...").press("Enter")
        await asyncio.sleep(1)


async def kompasiana_write(page: Page, article: ProcessedArticles) -> None:
    await page.goto(
        "https://www.kompasiana.com/muhammadaqilmaulana3384/dashboard/write"
    )
    await asyncio.sleep(5)
    await page.locator(".col-xs-2 > .dashboardInfo").first.click()
    await page.reload()
    await _select_category(page)
    await _fill_title(page, title=article.title)
    save_path = await download_image(article.image_url)
    await _fill_content(page, content=article.content_full, image_path=save_path)
    await _select_recommended_article(page)
    await _fill_teaser_and_recommended_tag(
        page, teaser=article.excerpt, tags=article.tags
    )
    await page.get_by_text("Simpan", exact=True).click()
