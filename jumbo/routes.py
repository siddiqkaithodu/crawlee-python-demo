from crawlee.basic_crawler import Router
from crawlee.playwright_crawler import PlaywrightCrawlingContext
from crawlee import Glob
from crawlee.models import Request
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
import asyncio
from contextlib import asynccontextmanager,suppress
router = Router[PlaywrightCrawlingContext]()

@asynccontextmanager
async def accept_cookies(page: Page):
    task = asyncio.create_task(page.locator('#onetrust-accept-btn-handler').click())
    try:
        yield
    finally:
        if not task.done():
            task.cancel()

        with suppress(asyncio.CancelledError, PlaywrightTimeoutError):
            await task

# <div class="banner-actions-container"><button id="onetrust-reject-all-handler">Weigeren</button> <button id="onetrust-accept-btn-handler">Akkoord</button></div>

@router.default_handler
async def default_handler(context: PlaywrightCrawlingContext) -> None:
    """Default request handler."""
    async with accept_cookies(context.page):
        all_links = await context.page.locator(".title-link").all()
        #  //*[@class="title-link"]
        await context.add_requests(
            [
                Request.from_url(f"https://www.jumbo.com{url}", label='product')
                for link in all_links
                if (url := await link.get_attribute('href'))
            ]
        )
        await context.page.locator('xpath=//button[(@class="secondary jum-button pagination-button") and @data-label="Volgende"]').click()
        await context.page.wait_for_load_state('networkidle')
        all_links = await context.page.locator(".title-link").all()
        await context.add_requests(
            [
                Request.from_url(f"https://www.jumbo.com{url}", label='product')
                for link in all_links
                if (url := await link.get_attribute('href'))
            ]
        )
    

@router.handler("product")
async def product(context: PlaywrightCrawlingContext) -> None:
    """listing request handler."""
    # Extract data from the page.
    async with accept_cookies(context.page):
        data = {
            'url': context.request.url,
            # 'title': context.soup.title.string,
            # 'html': await context.page.content()
        }

        # Push the extracted data to the default dataset.
        await context.push_data(data)
