# coding=utf-8
from urllib.parse import urljoin

from webcollector.fetch import Fetcher
from webcollector.generate import StatusGeneratorFilter
from webcollector.model import Page, CrawlDatums, CrawlDatum
from webcollector.utils import RegexRule


class Crawler(object):
    def __init__(self, db_manager, generator_filter=StatusGeneratorFilter()):
        self.db_manager = db_manager
        self.generator_filter = generator_filter
        self.fetcher = None
        self.num_threads = 10
        self.seeds = []

    def add_seed(self, url_or_datum):
        self.add_seed_and_return(url_or_datum)

    def add_seed_and_return(self, url_or_datum):
        crawl_datum = CrawlDatum.convert_from_item(url_or_datum)
        self.seeds.append(crawl_datum)
        return crawl_datum

    def add_seeds(self, urls_or_datums):
        self.add_seeds_and_return(urls_or_datums)

    def add_seeds_and_return(self, urls_or_datums):
        crawl_datums = CrawlDatum.convert_from_list(urls_or_datums)
        self.seeds.extend(crawl_datums)
        return crawl_datums

    def execute(self, page, detected):
        pass

    def start_once(self, depth_index):
        print("start crawling at depth {}".format(depth_index))
        self.db_manager.merge()
        self.fetcher = Fetcher(
            self.db_manager,
            execute_func=self.execute,
            generator_filter=self.generator_filter,
            num_threads=self.num_threads
        )
        self.fetcher.start()

    def start(self, num_depth):
        if len(self.seeds) == 0:
            raise Exception("Please add at least one seed")
        self.db_manager.inject(self.seeds)
        for depth_index in range(num_depth):
            self.start_once(depth_index)


class AutoDetectCrawler(Crawler):

    def __init__(self, db_manager, auto_detect):
        super().__init__(db_manager)
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

