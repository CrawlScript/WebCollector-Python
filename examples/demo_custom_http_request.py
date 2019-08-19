# coding=utf-8

import webcollector as wc
from webcollector.model import Page
from webcollector.plugin.net import HttpRequester

import requests


class MyRequester(HttpRequester):
    def get_response(self, crawl_datum):
        # custom http request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        }

        print("sending request with MyRequester")

        # send request and get response
        response = requests.get(crawl_datum.url, headers=headers)

        # update code
        crawl_datum.code = response.status_code

        # wrap http response as a Page object
        page = Page(crawl_datum,
                    response.content,
                    content_type=response.headers["Content-Type"],
                    http_charset=response.encoding)

        return page


class NewsCrawler(wc.RamCrawler):
    def __init__(self):
        super().__init__(auto_detect=True)
        self.num_threads = 10

        # set requester to enable MyRequester
        self.requester = MyRequester()

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