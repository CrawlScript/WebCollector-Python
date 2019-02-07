# coding=utf-8
from urllib.parse import urljoin

from webcollector.plugin.ram import RamCrawler


class MyCrawler(RamCrawler):
    def __init__(self):
        super().__init__(auto_detect=False)
        self.num_threads = 10
        for i in range(1, 4):
            self.add_seed_and_return("https://ruby-china.org/topics?page={}".format(i))\
                .set_type("list")
        # self.add_regex("https://ruby-china.org/topics\\?page=[0-9]+")

    def visit(self, page, detected):
        print(page.url)
        if page.type == "list":
            for a in page.select("div.title.media-heading>a[title]"):
                href = page.abs_url(a["href"])
                detected.append(href)
                print(a["title"].strip())
        else:
            print(page.doc.title)



crawler = MyCrawler()
crawler.start(10)
