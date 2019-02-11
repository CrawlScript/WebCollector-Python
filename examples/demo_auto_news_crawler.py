# coding=utf-8
import webcollector as wc


class NewsCrawler(wc.RamCrawler):
    def __init__(self):
        super().__init__(auto_detect=True)
        self.num_threads = 10
        self.add_seed("https://github.blog/")
        self.add_regex("https://github.blog/[0-9]+.*")

    def visit(self, page, detected):
        if page.match_url("https://github.blog/[0-9]+.*"):
            title = page.select("h1.lh-condensed")[0].text.strip()
            content = page.select("div.markdown-body")[0].text.replace("\n", " ").strip()
            print("\nURL: ", page.url)
            print("TITLE: ", title)
            print("CONTENT: ", content)


crawler = NewsCrawler()
crawler.start(10)
