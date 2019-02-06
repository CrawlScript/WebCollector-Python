# coding=utf-8
import chardet


# A CrawlDatum corresponds to a task description (usually for a webpage)
from bs4 import BeautifulSoup


class CrawlDatum(object):

    STATUS_DB_UNEXECUTED = 0
    STATUS_DB_FAILED = 1
    STATUS_DB_SUCCESS = 5
    CODE_NOT_SET = -1;

    def __init__(self, url, key=None, meta=None, code=CODE_NOT_SET, status=STATUS_DB_UNEXECUTED):
        self.url = url
        self.key = key if key is not None else url
        self.meta = meta
        self.code = code
        self.status = status


# A Page corresponds to the response of a http request
class Page(object):
    def __init__(self, crawl_datum, content, http_charset=None):
        self.crawl_datum = crawl_datum
        # self.code = code
        self.content = content
        self.http_charset = http_charset
        self._html = None
        self._detected_charset = None
        self._doc = None

    def code(self):
        return self.crawl_datum.code

    def doc(self):
        if self._doc is not None:
            return self._doc
        html = self.html()
        if html is None:
            return None
        self._doc = BeautifulSoup(html, features="html5lib")
        return self._doc

    def select(self, css_selector):
        soup = self.doc()
        return soup.select(css_selector)

    def html(self, charset=None):
        # cache
        if self._html is not None:
            return self._html
        # None Content
        if self.content is None:
            return None
        # Manual
        if charset is not None:
            return self.content.decode(charset)

        # Http Charset
        if self.http_charset is not None:
            return self.content.decode(self.http_charset)

        # detect
        if self._detected_charset is None:
            self._detected_charset = chardet.detect(self.content)['encoding']
            if self._detected_charset is None:
                return self.content.decode("utf-8")

        return self.content.decode(self._detected_charset)
