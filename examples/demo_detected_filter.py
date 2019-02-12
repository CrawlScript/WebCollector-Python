# coding=utf-8
import webcollector as wc
from webcollector.filter import Filter
import re


class RegexDetectedFilter(Filter):
    def filter(self, crawl_datum):
        if re.fullmatch("https://github.blog/2019-02.*", crawl_datum.url):
            return crawl_datum
        else:
            print("filtered by detected_filter: {}".format(crawl_datum.brief_info()))
            return None


class NewsCrawler(wc.RamCrawler):
    def __init__(self):
        super().__init__(auto_detect=True, detected_filter=RegexDetectedFilter())
        self.num_threads = 10
        self.add_seed("https://github.blog/")

    def visit(self, page, detected):

        detected.extend(page.links("https://github.blog/[0-9]+.*"))

        if page.match_url("https://github.blog/[0-9]+.*"):
            title = page.select("h1.lh-condensed")[0].text.strip()
            content = page.select("div.markdown-body")[0].text.replace("\n", " ").strip()
            print("\nURL: ", page.url)
            print("TITLE: ", title)
            print("CONTENT: ", content[:50], "...")


crawler = NewsCrawler()
crawler.start(10)
