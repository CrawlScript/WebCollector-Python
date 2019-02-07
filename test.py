# coding=utf-8
from webcollector.plugin.ram import RamCrawler


class MyCrawler(RamCrawler):
    def __init__(self):
        super().__init__(True)
        self.num_threads = 10
        self.add_seed_and_return("https://ruby-china.org/topics?page=1")
        self.add_regex("https://ruby-china.org/topics\\?page=[0-9]+")

    def visit(self, page, detected):
        print(page.url)
        for a in page.select("div.title.media-heading>a[title]"):
            print(a["title"].strip())


crawler = MyCrawler()
crawler.start(10)
