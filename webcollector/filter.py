# coding=utf-8
class Filter(object):
    def filter(self, crawl_datum):
        return None


class HistoryFilter(Filter):
    def __init__(self, history):
        self.history = history

    def filter(self, crawl_datum):
        if crawl_datum.key in self.history:
            return crawl_datum
        else:
            return None
