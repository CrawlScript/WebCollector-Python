# coding=utf-8
from webcollector.model import CrawlDatum
from webcollector.filter import Filter


class Generator(object):

    def __init__(self):
        self.num_generated = 0
        self.generator_filter = None

    def next(self):
        while True:
            crawl_datum = self._next()
            if crawl_datum is None:
                return crawl_datum
            else:
                if self.generator_filter is None:
                    return crawl_datum
                else:
                    crawl_datum = self.generator_filter.filter(crawl_datum)
                    if crawl_datum is None:
                        continue
                    else:
                        self.num_generated += 1
                        return crawl_datum

    def _next(self):
        return None


class StatusGeneratorFilter(Filter):
    def filter(self, crawl_datum):
        if crawl_datum.status != CrawlDatum.STATUS_DB_SUCCESS:
            return crawl_datum
        else:
            return None