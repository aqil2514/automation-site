from playwright.async_api import Page

from .write import kompasiana_write

from .login import kompasiana_login


async def start_kompasiana(page: Page) -> None:
    await kompasiana_login(page)
    await kompasiana_write(page)
