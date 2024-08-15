import asyncio

from crawlee.playwright_crawler.playwright_crawler import PlaywrightCrawler
# from crawlee.proxy_configuration import ProxyConfiguration
from .routes import router
# proxies = ProxyConfiguration(proxy_urls=["http://account-scrapehero-pipeline-datateam_israel:38oDsxme7321@ip.nimbleway.com:7000",
#       "http://account-scrapehero-pipeline-autralia_sticky:mS77198T5fpG@ip.nimbleway.com:7000",
#       "http://account-scrapehero-pipeline-br:H1t96de1Q12h@beta.nimbleway.com:7000",
#       "http://account-scrapehero-pipeline-ca:f14op5T0I9a9@beta.nimbleway.com:7000",
#       "http://account-scrapehero-pipeline-de:g6m83j7s96xS@beta.nimbleway.com:7000",
#       "http://account-scrapehero-pipeline-es:49YI3GK0nf16@beta.nimbleway.com:7000",
#       "http://account-scrapehero-pipeline-fr:67xo960d6ePu@beta.nimbleway.com:7000",
#       "http://account-scrapehero-pipeline-fr:67xo960d6ePu@beta.nimbleway.com:7000",
#       "http://account-scrapehero-pipeline-nimble_india:2Z8k4CTX016d@beta.nimbleway.com:7000",])

async def main() -> None:
    """The crawler entry point."""
    crawler = PlaywrightCrawler(
        request_handler=router,
        # max_requests_per_crawl=5,
        # proxy_configuration=proxies
        headless=False
    )

    await crawler.run(
        [
            'https://www.jumbo.com/producten/',
        ]
    )
    
    await crawler.export_data('products.csv')


if __name__ == '__main__':
    asyncio.run(main())
