from typing import Literal
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

from src.crawlers.kompasiana import start_kompasiana


async def run_scraper(action_code: Literal["kompasiana"]) -> None:
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        if action_code == "kompasiana":
            return await start_kompasiana(page)
