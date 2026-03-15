import asyncio

from playwright.async_api import Page


async def _select_category(page: Page) -> None:
    await page.locator("span").filter(has_text="Pilih Kategori").click()
    await page.locator("span").filter(has_text="Financial").click()


async def _fill_title(page: Page) -> None:
    await page.get_by_role("textbox", name="Judul").click()
    await page.get_by_role("textbox", name="Judul").fill("Testing From Python")


async def _fill_content(page: Page) -> None:
    await page.locator(".fr-element").click()
    await page.locator(".fr-element").fill(
        "Di sini nanti ada konten yang bakal ditulis otomatis"
    )


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


async def _fill_teaser_and_recommended_tag(page: Page) -> None:
    await page.get_by_role("textbox", name="Tulis teaser untuk menarik").click()
    await page.get_by_role("textbox", name="Tulis teaser untuk menarik").fill(
        "Nanti ini juga otomatis"
    )
    await page.get_by_text("REKOMENDASI", exact=True).click()


async def kompasiana_write(page: Page) -> None:
    await page.goto(
        "https://www.kompasiana.com/muhammadaqilmaulana3384/dashboard/write"
    )
    await asyncio.sleep(5)
    await page.locator(".col-xs-2 > .dashboardInfo").first.click()
    await page.reload()
    await _select_category(page)
    await _fill_title(page)
    await _fill_content(page)
    await _select_recommended_article(page)
    await _fill_teaser_and_recommended_tag(page)
    await page.get_by_text("Simpan", exact=True).click()
