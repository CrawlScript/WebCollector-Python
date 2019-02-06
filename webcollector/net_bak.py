# coding=utf-8
import requests
import threading
from threading import Thread
from multiprocessing.dummy import Pool
from webcollector.model import CrawlDatum, Page
import queue


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




import time

start = time.time()

feeding = True
fetch_queue = queue.Queue()

requester = Requester()


def visit(page):
    print(len(page.html()))

pool_size = 20
count = 0
def fetch_thread_func():
    while feeding or not fetch_queue.empty():
        try:
            crawl_datum = fetch_queue.get(block=False)
        except queue.Empty:
            continue
        page = requester.get_response(crawl_datum=crawl_datum)
        visit(page)
        global count
        count += 1
        print(count, "--------------")

def feed_thread_func():
    global feeding
    feeding = True
    for i in range(100):
        fetch_queue.put(CrawlDatum("http://www.hfut.edu.cn"))
    feeding = False

Thread(target=feed_thread_func).start()

threads = [Thread(target=fetch_thread_func) for _ in range(pool_size)]
for thread in threads:
    thread.start()
# for thread in threads:
#     thread.join()





end = time.time()
print(end - start)


