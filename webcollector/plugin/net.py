# coding=utf-8
from webcollector.config import DEFAULT_USER_AGENT
from webcollector.model import Page
from webcollector.net import Requester
import aiohttp


class HttpRequester(Requester):

    def __init__(self):
        self.session = None

    def create_async_context_manager(self):
        self.session = aiohttp.ClientSession()
        return self.session

    def request(self, crawl_datum):
        return self.session.get(
            crawl_datum.url,
            headers={"User-Agent": DEFAULT_USER_AGENT}
        )

    async def get_response(self, crawl_datum):
        # async with self.session.get(crawl_datum.url) as response:
        async with self.request(crawl_datum) as response:
            code = response.status
            content = await response.content.read()
            encoding = response.get_encoding()
            content_type = response.content_type
        crawl_datum.code = code
        page = Page(crawl_datum, content, content_type=content_type, http_charset=encoding)
        return page




