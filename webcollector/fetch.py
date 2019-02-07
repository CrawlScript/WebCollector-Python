# coding=utf-8
import queue
import asyncio
import aiohttp

from webcollector.model import Page, CrawlDatums, CrawlDatum


class Fetcher(object):
    def __init__(self, db_manager, execute_func, generator_filter=None, num_threads=10):
        self.fetch_queue = None
        self.feed_stopped = None
        self.generator = None
        self.generator_filter = generator_filter
        self.feeder = None
        self.buffer_size = 1000
        self.db_manager = db_manager

        self.execute_func = execute_func
        self.num_threads = num_threads

    async def async_start(self):
        self.fetch_queue = queue.Queue()
        self.feed_stopped = False
        self.db_manager.init_fetch_and_detect()
        self.generator = self.db_manager.create_generator()
        self.generator.generator_filter = self.generator_filter
        async with aiohttp.ClientSession() as session:
            coroutines = [self.fetch_coroutine(session, self.execute_func) for _ in range(self.num_threads)]
            await asyncio.gather(*coroutines)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_start())

    def feed(self):
        for i in range(self.buffer_size):
            crawl_datum = self.generator.next()
            if crawl_datum is None:
                self.feed_stopped = True
                return
            else:
                self.fetch_queue.put(crawl_datum)

    async def fetch_coroutine(self, session, execute_func):
        while True:
            if self.fetch_queue.empty():
                if self.feed_stopped:
                    break
                self.feed()
            else:
                crawl_datum = self.fetch_queue.get(block=False)
                async with session.get(crawl_datum.url) as response:
                    code = response.status
                    content = await response.content.read()
                    encoding = response.get_encoding()
                    content_type = response.content_type

                    crawl_datum.code = code
                page = Page(crawl_datum, content, content_type=content_type, http_charset=encoding)
                detected = CrawlDatums()
                execute_func(page, detected)

                crawl_datum.status = CrawlDatum.STATUS_DB_SUCCESS
                self.db_manager.write_fetch(crawl_datum)

                for detected_crawl_datum in detected:
                    self.db_manager.write_detect(detected_crawl_datum)


