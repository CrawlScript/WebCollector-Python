# coding=utf-8
import queue
import asyncio
import logging
from webcollector.model import Page, CrawlDatums, CrawlDatum

logger = logging.getLogger(__name__)


class Fetcher(object):
    def __init__(self,
                 db_manager,
                 requester,
                 execute_func,
                 generator_filter=None,
                 detected_filter=None,
                 num_threads=10):
        self.fetch_queue = None
        self.feed_stopped = None
        self.generator = None
        self.generator_filter = generator_filter
        self.detected_filter = detected_filter
        self.feeder = None
        self.buffer_size = 1000
        self.db_manager = db_manager

        self.requester = requester
        self.execute_func = execute_func
        self.num_threads = num_threads

    async def async_start(self):
        self.fetch_queue = queue.Queue()
        self.feed_stopped = False
        self.db_manager.open()
        self.db_manager.init_fetch_and_detect()
        self.generator = self.db_manager.create_generator()
        self.generator.generator_filter = self.generator_filter
        async with self.requester.create_async_context_manager():
            coroutines = [self.fetch_coroutine(self.execute_func) for _ in range(self.num_threads)]
            await asyncio.gather(*coroutines)
        self.db_manager.close()

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_start())
        return self.generator.num_generated

    def feed(self):
        for i in range(self.buffer_size):
            crawl_datum = self.generator.next()
            if crawl_datum is None:
                self.feed_stopped = True
                return
            else:
                self.fetch_queue.put(crawl_datum)

    async def fetch_coroutine(self, execute_func):
        while True:
            if self.fetch_queue.empty():
                if self.feed_stopped:
                    break
                self.feed()
            else:
                crawl_datum = self.fetch_queue.get(block=False)
                try:
                    page = await self.requester.get_response(crawl_datum)
                    detected = CrawlDatums()
                    execute_func(page, detected)

                    crawl_datum.status = CrawlDatum.STATUS_DB_SUCCESS

                    if self.detected_filter is not None:
                        filtered_detected = CrawlDatums()
                        for detected_crawl_datum in detected:
                            detected_crawl_datum = self.detected_filter.filter(detected_crawl_datum)
                            if detected_crawl_datum is not None:
                                filtered_detected.append(detected_crawl_datum)
                    else:
                        filtered_detected = detected

                    for detected_crawl_datum in filtered_detected:
                        self.db_manager.write_detect(detected_crawl_datum)
                    logger.info("done: {}".format(crawl_datum.brief_info()))
                except Exception as e:
                    logger.error("failed: {}".format(crawl_datum.brief_info()), exc_info=True)
                    crawl_datum.status = CrawlDatum.STATUS_DB_FAILED

                crawl_datum.num_fetched += 1
                self.db_manager.write_fetch(crawl_datum)
