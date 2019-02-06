# coding=utf-8
from webcollector.model import CrawlDatum
import time

from webcollector.plugin.ram import RamCrawler


def next_crawl_datum():
    for i in range(1, 41):
        yield CrawlDatum()


class MyCrawler(RamCrawler):

    def __init__(self):
        super().__init__()
        self.num_threads = 10
        for i in range(1, 41):
            seed_url = "https://ruby-china.org/topics?page={}".format(i)
            self.add_seed(seed_url)

    def execute(self, page, detected):
        titles = [a["title"].strip() for a in page.select("div.title.media-heading>a[title]")]
        print(titles)


start = time.time()
crawler = MyCrawler()
crawler.start_once(1)
print("time: ", time.time() - start)
