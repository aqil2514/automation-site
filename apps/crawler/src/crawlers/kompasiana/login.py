import asyncio

from playwright.async_api import Page
from src.core.config import config_env


async def kompasiana_login(page: Page) -> None:
    await page.goto("https://www.kompasiana.com/muhammadaqilmaulana3384")
    await page.get_by_role("link", name="MASUK").click()
    await page.get_by_role("textbox", name="Akun KG Media ID").click()
    await page.get_by_role("textbox", name="Akun KG Media ID").fill(
        config_env.KOMPASIANA_EMAIL
    )
    await page.get_by_role("textbox", name="Password").click()
    await page.get_by_role("textbox", name="Password").fill(
        config_env.KOMPASIANA_PASSWORD
    )
    await page.get_by_role("button", name="Login").click()

    await page.wait_for_load_state("networkidle")

    await asyncio.sleep(10)
