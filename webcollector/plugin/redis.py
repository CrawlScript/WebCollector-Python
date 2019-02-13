# coding=utf-8
from redis import StrictRedis

from webcollector.crawler import AutoDetectCrawler
from webcollector.db_manager import DBManager
from webcollector.generate import Generator
from webcollector.model import CrawlDatum


class RedisDBGenerator(Generator):

    def __init__(self, redis_db_manager):
        super().__init__()
        self.history_keys = set()
        self.iter = redis_db_manager.redis_client.hscan_iter(
            redis_db_manager.crawl_db
        )

    def _next(self) -> CrawlDatum:
        try:
            while True:
                key, crawl_datum_json = next(self.iter)
                if key in self.history_keys:
                    continue
                else:
                    self.history_keys.add(key)
                return CrawlDatum.from_json(crawl_datum_json)
        except StopIteration:
            return None


class RedisDBManager(DBManager):
    def __init__(self, redis_client: StrictRedis, db_prefix):
        self.redis_client = redis_client
        self.db_prefix = db_prefix
        self.crawl_db = "{}_crawl".format(db_prefix)
        self.fetch_db = "{}_fetch".format(db_prefix)
        self.detect_db = "{}_detect".format(db_prefix)

    def open(self):
        pass

    def close(self):
        pass

    def clear(self):
        self.redis_client.delete(self.crawl_db)
        self.redis_client.delete(self.fetch_db)
        self.redis_client.delete(self.detect_db)

    def inject(self, seeds, forced=False):
        for seed in seeds:
            if isinstance(seed, str):
                seed = CrawlDatum(seed)
            if not forced and self.redis_client.hexists(self.crawl_db, seed.key):
                continue
            self.redis_client.hset(self.crawl_db, seed.key, seed.to_json())

    def create_generator(self):
        return RedisDBGenerator(self)

    def init_fetch_and_detect(self):
        pass

    def write_fetch(self, crawl_datum):
        self.redis_client.hset(self.fetch_db, crawl_datum.key, crawl_datum.to_json())

    def write_detect(self, crawl_datum):
        self.redis_client.hset(self.detect_db, crawl_datum.key, crawl_datum.to_json())

    def merge(self):
        print("merging......")
        if self.redis_client.exists(self.fetch_db):
            for _, crawl_datum_json in self.redis_client.hscan_iter(self.fetch_db):
                crawl_datum = CrawlDatum.from_json(crawl_datum_json)
                self.redis_client.hset(self.crawl_db, crawl_datum.key, crawl_datum.to_json())
            self.redis_client.delete(self.fetch_db)

        if self.redis_client.exists(self.detect_db):
            for key, crawl_datum_json in self.redis_client.hscan_iter(self.detect_db):
                if not self.redis_client.hexists(self.crawl_db, key):
                    crawl_datum = CrawlDatum.from_json(crawl_datum_json)
                    self.redis_client.hset(self.crawl_db, crawl_datum.key, crawl_datum.to_json())
            self.redis_client.delete(self.detect_db)


class RedisCrawler(AutoDetectCrawler):
    def __init__(self, redis_client, db_prefix, auto_detect, **kwargs):
        super().__init__(RedisDBManager(redis_client, db_prefix), auto_detect, **kwargs)

