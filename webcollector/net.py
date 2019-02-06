# coding=utf-8
import requests
import threading
from threading import Thread
from multiprocessing.dummy import Pool
from webcollector.model import CrawlDatum, Page
import queue
import time
import aiohttp
import asyncio

class Requester(object):
    def get_response(self, url=None, crawl_datum: CrawlDatum=None):
        if url is not None and crawl_datum is not None:
            raise Exception("both url and crawl_datum is not None")
        if crawl_datum is None:
            crawl_datum = CrawlDatum(url)

        res = requests.get(crawl_datum.url)
        crawl_datum.code = res.status_code
        page = Page(crawl_datum, res.content, http_charset=res.encoding)
        return page



