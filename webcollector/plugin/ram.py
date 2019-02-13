# coding=utf-8
from webcollector.crawler import AutoDetectCrawler
from webcollector.db_manager import DBManager
from webcollector.generate import Generator
from webcollector.model import CrawlDatum


class RamDB(object):
    def __init__(self):
        self.crawl_db = {}
        self.fetch_db = None
        self.detect_db = None


class RamDBGenerator(Generator):

    def __init__(self, ram_db):
        super().__init__()
        self.ram_db = ram_db
        self.iter = iter(self.ram_db.crawl_db.values())

    def _next(self) -> CrawlDatum:
        try:
            return next(self.iter)
        except StopIteration:
            return None


class RamDBManager(DBManager):
    def __init__(self, ram_db):
        self.ram_db = ram_db

    def inject(self, seeds, forced=False):
        for seed in seeds:
            if isinstance(seed, str):
                seed = CrawlDatum(seed)
            if not forced and seed.key in self.ram_db.crawl_db:
                continue
            self.ram_db.crawl_db[seed.key] = seed

    def create_generator(self):
        return RamDBGenerator(self.ram_db)

    def init_fetch_and_detect(self):
        self.ram_db.fetch_db = {}
        self.ram_db.detect_db = {}

    def write_fetch(self, crawl_datum):
        self.ram_db.fetch_db[crawl_datum.key] = crawl_datum

    def write_detect(self, crawl_datum):
        self.ram_db.detect_db[crawl_datum.key] = crawl_datum

    def merge(self):
        print("merging......")
        if self.ram_db.fetch_db is not None:
            for crawl_datum in self.ram_db.fetch_db.values():
                self.ram_db.crawl_db[crawl_datum.key] = crawl_datum
            self.ram_db.fetch_db = None

        if self.ram_db.detect_db is not None:
            for crawl_datum in self.ram_db.detect_db.values():
                if crawl_datum.key not in self.ram_db.crawl_db:
                    self.ram_db.crawl_db[crawl_datum.key] = crawl_datum
            self.ram_db.detect_db = None


class RamCrawler(AutoDetectCrawler):
    def __init__(self, auto_detect, **kwargs):
        self.ram_db = RamDB()
        super().__init__(RamDBManager(self.ram_db), auto_detect, **kwargs)

