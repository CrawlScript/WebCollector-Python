# coding=utf-8
from webcollector.crawl import Crawler
from webcollector.dbmanager import DBManager
from webcollector.generate import StatusGenerator
from webcollector.model import CrawlDatum


class RamDB(object):
    def __init__(self):
        self.crawl_db = {}
        self.fetch_db = None
        self.detect_db = None


class RamDBGenerator(StatusGenerator):

    def __init__(self, ram_db):
        self.ram_db = ram_db
        self.iter = None

    def _next(self) -> CrawlDatum:
        if self.iter is None:
            self.iter = iter(self.ram_db.crawl_db.values())
        try:
            return next(self.iter)
        except StopIteration:
            return None


class RamDBManager(DBManager):
    def __init__(self, ram_db):
        self.ram_db = ram_db

    def inject(self, seeds):
        for seed in seeds:
            if isinstance(seed, str):
                seed = CrawlDatum(seed)
            self.ram_db.crawl_db[seed.key] = seed

    def write_crawl(self, crawl_datum):
        if crawl_datum.key not in self.ram_db.crawl_db:
            self.ram_db.crawl_db[crawl_datum.key] = crawl_datum

    def init_fetch_and_detect(self):
        self.ram_db.fetch_db = {}
        self.ram_db.detect_db = {}

    def close_fetch_and_detect(self):
        pass

    def write_fetch(self, crawl_datum):
        self.ram_db.fetch_db[crawl_datum.key] = crawl_datum

    def write_detect(self, crawl_datum):
        self.ram_db.detect_db[crawl_datum.key] = crawl_datum


class RamCrawler(Crawler):
    def __init__(self, ):
        self.ram_db = RamDB()
        super().__init__(RamDBManager(self.ram_db), RamDBGenerator(self.ram_db))

