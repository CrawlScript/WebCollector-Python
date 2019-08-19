# coding=utf-8
import webcollector as wc
import time


class RubyChinaCrawler(wc.RamCrawler):
    def __init__(self):
        super().__init__(auto_detect=False)
        self.num_threads = 10
        self.add_seeds(["https://ruby-china.org/topics?page={}".format(i) for i in range(1, 40)])

    def visit(self, page, detected):
        print("start_visit", page.url)
        time.sleep(4)
        print("end_visit", page.url)


crawler = RubyChinaCrawler()
start = time.time()
crawler.start(10)
print(time.time() - start)


