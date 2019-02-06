# coding=utf-8
from webcollector.model import CrawlDatum


class Generator(object):
    def next(self):
        pass


class StatusGenerator(Generator):
    def next(self):
        while True:
            crawl_datum = self._next()
            if crawl_datum is None:
                return None
            if crawl_datum.status == CrawlDatum.STATUS_DB_SUCCESS:
                continue
            else:
                return crawl_datum

    def _next(self) -> CrawlDatum:
        return None