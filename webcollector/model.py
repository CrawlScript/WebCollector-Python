# coding=utf-8
from urllib.parse import urljoin
import chardet
from bs4 import BeautifulSoup
import json


# A CrawlDatum corresponds to a task description (usually for a webpage)
from webcollector.utils import url_matches


class CrawlDatum(object):
    STATUS_DB_UNEXECUTED = 0
    STATUS_DB_FAILED = 1
    STATUS_DB_SUCCESS = 5
    CODE_NOT_SET = -1

    META_KEY_SYS_TYPE = "sys_type"

    def __init__(self, url,
                 key=None,
                 type=None,
                 meta_dict=None,
                 code=CODE_NOT_SET,
                 status=STATUS_DB_UNEXECUTED,
                 num_fetched=0):
        self.url = url
        self.key = key if key is not None else url
        self.type = type
        self.meta_dict = meta_dict
        self.code = code
        self.status = status
        self.num_fetched = num_fetched

    def set_key(self, key):
        self.key = key
        return self

    def set_type(self, type):
        self.type = type
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

    def match_type(self, type):
        return self.type == type

    def match_url(self, url_regex):
        return url_matches(self.url, url_regex)

    @classmethod
    def convert_from_item(cls, url_or_datum):
        if isinstance(url_or_datum, CrawlDatum):
            return url_or_datum
        else:
            return CrawlDatum(url_or_datum)

    def brief_info(self):
        infos = []
        if self.code != CrawlDatum.CODE_NOT_SET:
            infos.append("[{}]".format(self.code))
        infos.append("Key: {} (URL: {})".format(self.key, self.url))
        return " ".join(infos)

    def to_dict(self):
        dict_data = {
            "url": self.url,
            "key": self.key,
            "type": self.type,
            "meta_dict": self.meta_dict,
            "code": self.code,
            "status": self.status,
            "num_fetched": self.num_fetched
        }
        return dict_data

    @classmethod
    def from_dict(cls, dict_data):
        return CrawlDatum(
            url=dict_data["url"],
            key=dict_data["key"],
            type=dict_data["type"],
            meta_dict=dict_data["meta_dict"],
            code=dict_data["code"],
            status=dict_data["status"],
            num_fetched=dict_data["num_fetched"]
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str):
        return CrawlDatum.from_dict(json.loads(json_str))


class CrawlDatums(list):

    def append(self, url_or_datum):
        if isinstance(url_or_datum, CrawlDatum):
            crawl_datum = url_or_datum
        else:
            crawl_datum = CrawlDatum(url_or_datum)
        super().append(crawl_datum)
        return crawl_datum

    def extend(self, url_or_datums):
        crawl_datums = []
        for url_or_datum in url_or_datums:
            crawl_datums.append(self.append(url_or_datum))
        return crawl_datums

    def set_type(self, type):
        for crawl_datum in self:
            crawl_datum.type = type

    def set_meta_item(self, meta_key, meta_value):
        for crawl_datum in self:
            crawl_datum.set_meta_item(meta_key, meta_value)

    @classmethod
    def convert_from_list(cls, urls_or_datums):
        return [CrawlDatum.convert_from_item(item) for item in urls_or_datums]


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

    def abs_url(self, abs_or_relative_url):
        return urljoin(self.url, abs_or_relative_url)

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
        # cache
        if self._html is not None:
            return self._html
        self._html = self.decode_content()
        return self._html

    @property
    def type(self):
        return self.crawl_datum.type

    def links(self, url_regex=None):
        a_eles = self.doc.select("a[href]")
        urls = [self.abs_url(a_ele["href"]) for a_ele in a_eles]
        if url_regex is None:
            return urls
        else:
            urls = [url for url in urls if url_matches(url, url_regex)]
            return urls

    def decode_content(self, charset=None):
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

    def match_type(self, type):
        return self.crawl_datum.match_type(type)

    def match_url(self, url_regex):
        return self.crawl_datum.match_url(url_regex)
