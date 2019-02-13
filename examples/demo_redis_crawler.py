# coding=utf-8
from redis import StrictRedis
import webcollector as wc


class NewsCrawler(wc.RedisCrawler):

    def __init__(self):
        super().__init__(redis_client=StrictRedis("127.0.0.1"),
                         db_prefix="news",
                         auto_detect=True)
        self.num_threads = 10
        self.resumable = True  # you can resume crawling after shutdown
        self.add_seed("https://github.blog/")
        self.add_regex("+https://github.blog/[0-9]+.*")
        self.add_regex("-.*#.*")  # do not detect urls that contain "#"

    def visit(self, page, detected):
        if page.match_url("https://github.blog/[0-9]+.*"):
            title = page.select("h1.lh-condensed")[0].text.strip()
            content = page.select("div.markdown-body")[0].text.replace("\n", " ").strip()
            print("\nURL: ", page.url)
            print("TITLE: ", title)
            print("CONTENT: ", content[:50], "...")


crawler = NewsCrawler()
crawler.start(10)
