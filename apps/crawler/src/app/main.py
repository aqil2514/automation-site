import asyncio

from playwright.async_api import async_playwright
from playwright_stealth import Stealth

from src.crawlers.kompasiana import start_kompasiana


async def main():
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await start_kompasiana(page)

        await asyncio.sleep(5)
        # await browser.close()


asyncio.run(main())
