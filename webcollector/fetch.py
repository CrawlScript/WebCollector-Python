# coding=utf-8
import queue
import asyncio
import aiohttp

from webcollector.model import Page


class Fetcher(object):
    def __init__(self, db_manager, generator):
        self.fetch_queue = None
        self.feed_stopped = None
        self.generator = None
        self.feeder = None
        self.buffer_size = 1000
        self.db_manager = db_manager
        self.generator = generator

    async def async_start(self, execute_func, num_threads):
        self.fetch_queue = queue.Queue()
        self.feed_stopped = False
        self.db_manager.init_fetch_and_detect()
        async with aiohttp.ClientSession() as session:
            coroutines = [self.fetch_coroutine(session, execute_func) for _ in range(num_threads)]
            await asyncio.gather(*coroutines)

    def start(self, execute_func, num_threads=10):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_start(execute_func, num_threads))

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

                    crawl_datum.code = code
                page = Page(crawl_datum, content, encoding)
                detected = []
                execute_func(page, detected)

                self.db_manager.write_fetch(crawl_datum)
                for detected_crawl_datum in detected:
                    self.db_manager.write_detect(detected_crawl_datum)

