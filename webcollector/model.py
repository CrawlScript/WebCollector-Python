# coding=utf-8
import chardet


# A CrawlDatum corresponds to a task description (usually for a webpage)
from bs4 import BeautifulSoup


class CrawlDatum(object):

    STATUS_DB_UNEXECUTED = 0
    STATUS_DB_FAILED = 1
    STATUS_DB_SUCCESS = 5
    CODE_NOT_SET = -1;

    def __init__(self, url, key=None, meta_dict=None, code=CODE_NOT_SET, status=STATUS_DB_UNEXECUTED):
        self.url = url
        self.key = key if key is not None else url
        self.meta_dict = meta_dict
        self.code = code
        self.status = status

    def set_key(self, key):
        self.key = key
        return self

    def set_url(self, url):
        self.url = url
        return self

    def set_meta_dict(self, meta_dict):
        self.meta_dict = meta_dict
        return self.meta_dict

    def set_meta_item(self, meta_key, meta_value):
        if self.meta_dict is None:
            self.meta_dict = {}
        self.meta_dict[meta_key] = meta_value
        return self

    @classmethod
    def convert_from_item(cls, url_or_datum):
        if isinstance(url_or_datum, CrawlDatum):
            return url_or_datum
        else:
            return CrawlDatum(url_or_datum)

    @classmethod
    def convert_from_list(cls, urls_or_datums):
        return [CrawlDatum.convert_from_item(item) for item in urls_or_datums]


class CrawlDatums(list):

    def append(self, url_or_datum):
        self.append_and_return(url_or_datum)

    def append_and_return(self, url_or_datum):
        if isinstance(url_or_datum, CrawlDatum):
           crawl_datum = url_or_datum
        else:
            crawl_datum = CrawlDatum(url_or_datum)
        super().append(crawl_datum)
        return crawl_datum

    def extend_and_return(self, url_or_datums):
        crawl_datums = []
        for url_or_datum in url_or_datums:
            crawl_datums.append(self.append_and_return(url_or_datum))
        return crawl_datums

    def extend(self, url_or_datums):
        self.extend_and_return(url_or_datums)





# A Page corresponds to the response of a http request
class Page(object):
    def __init__(self, crawl_datum, content, content_type=None, http_charset=None):
        self.crawl_datum = crawl_datum
        # self.code = code
        self.content = content
        self.content_type = content_type
        self.http_charset = http_charset
        self._html = None
        self._detected_charset = None
        self._doc = None

    @property
    def code(self):
        return self.crawl_datum.code

    @property
    def url(self):
        return self.crawl_datum.url

    @property
    def doc(self):
        if self._doc is not None:
            return self._doc
        html = self.html
        if html is None:
            return None
        self._doc = BeautifulSoup(html, features="html5lib")
        return self._doc

    def select(self, css_selector):
        soup = self.doc
        return soup.select(css_selector)

    @property
    def html(self):
        return self.decode_content()

    def decode_content(self, charset=None):
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
