from crawlee.basic_crawler import Router
from crawlee.playwright_crawler import PlaywrightCrawlingContext
from crawlee import Glob
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
        # await asyncio.sleep(10)
        # await context.enqueue_links()
        await context.enqueue_links(
        include=[Glob('https://www.jumbo.com/producten/**')],
        label="product"
    )
    

@router.handler("product")
async def product(context: PlaywrightCrawlingContext) -> None:
    """listing request handler."""
    # Extract data from the page.
    async with accept_cookies(context.page):
        data = {
            'url': context.request.url,
            # 'title': context.soup.title.string,
            'html': await context.page.content()
        }

        # Push the extracted data to the default dataset.
        await context.push_data(data)
