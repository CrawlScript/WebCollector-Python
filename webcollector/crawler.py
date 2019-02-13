# coding=utf-8
from urllib.parse import urljoin

from webcollector.fetch import Fetcher
from webcollector.generate import StatusGeneratorFilter
from webcollector.model import Page, CrawlDatums
from webcollector.plugin.net import HttpRequester
from webcollector.utils import RegexRule

import logging
import time

logger = logging.getLogger(__name__)


class Crawler(object):
    def __init__(self,
                 db_manager,
                 requester=HttpRequester(),
                 generator_filter=StatusGeneratorFilter(),
                 detected_filter=None):
        self.db_manager = db_manager
        self.requester = requester
        self.generator_filter = generator_filter
        self.detected_filter = detected_filter
        self.fetcher = None
        self.num_threads = 10
        self.resumable = None

        self.seeds = CrawlDatums()
        self.forced_seeds = CrawlDatums()

    def add_seed(self, url_or_datum, type=None, forced=False):
        if forced:
            return self.forced_seeds.append(url_or_datum).set_type(type)
        else:
            return self.seeds.append(url_or_datum).set_type(type)

    def add_seeds(self, urls_or_datums, type=None, forced=False):
        crawl_datums = []
        for url_or_datum in urls_or_datums:
            crawl_datum = self.add_seed(url_or_datum, type=type, forced=forced)
            crawl_datums.append(crawl_datum)
        return crawl_datums

    def inject(self):
        self.db_manager.inject(self.seeds, forced=False)
        self.db_manager.inject(self.forced_seeds, forced=True)

    # def add_seed_and_return(self, url_or_datum):
    # crawl_datum = CrawlDatum.convert_from_item(url_or_datum)
    # self.seeds.append(crawl_datum)
    # return crawl_datum

    # def add_seeds_and_return(self, urls_or_datums):
    #     crawl_datums = CrawlDatum.convert_from_list(urls_or_datums)
    #     self.seeds.extend(crawl_datums)
    #     return crawl_datums

    def execute(self, page, detected):
        pass

    def start_once(self, depth_index):
        self.db_manager.merge()
        self.fetcher = Fetcher(
            self.db_manager,
            self.requester,
            execute_func=self.execute,
            generator_filter=self.generator_filter,
            detected_filter=self.detected_filter,
            num_threads=self.num_threads
        )
        return self.fetcher.start()

    def start(self, depth):
        if not self.resumable:
            self.db_manager.clear()
        if len(self.seeds) == 0 and len(self.forced_seeds) == 0:
            raise Exception("Please add at least one seed")
        self.inject()
        for depth_index in range(depth):
            print("start depth {}".format(depth_index))
            start_time = time.time()
            num_generated = self.start_once(depth_index)
            cost_time = time.time() - start_time
            logger.info("depth {} finish: \n\ttotal urls:\t{}\n\ttotal time:\t{} seconds"
                        .format(depth_index, num_generated, cost_time))
            if num_generated == 0:
                break


class AutoDetectCrawler(Crawler):

    def __init__(self, db_manager, auto_detect, **kwargs):
        super().__init__(db_manager, **kwargs)
        self.auto_detect = auto_detect
        self.regex_rule = RegexRule()

    def add_regex(self, regex):
        self.regex_rule.add(regex)

    def execute(self, page, detected):
        self.visit(page, detected)
        if self.auto_detect:
            self.detect_links(page, detected)

    def visit(self, page, detected):
        pass

    def detect_links(self, page: Page, detected):
        if page.content_type is not None and "text/html" in page.content_type:
            link_eles = page.select("a[href]")
            for link_ele in link_eles:
                href = link_ele["href"]
                abs_href = urljoin(page.url, href)
                if self.regex_rule.matches(abs_href):
                    detected.append(abs_href)
