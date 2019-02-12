# WebCollector-Python

WebCollector-Python is an open source web crawler framework based on Python.It provides some simple interfaces for crawling the Web,you can setup a multi-threaded web crawler in less than 5 minutes.


## HomePage

[https://github.com/CrawlScript/WebCollector-Python](https://github.com/CrawlScript/WebCollector-Python)

## WebCollector Java Version

For better efficiency, WebCollector Java Version is recommended: [https://github.com/CrawlScript/WebCollector](https://github.com/CrawlScript/WebCollector)


## Installation

### pip

```bash
pip install https://github.com/CrawlScript/WebCollector-Python/archive/master.zip
```

## Example Index


### Basic

+ [demo_auto_news_crawler.py](examples/demo_auto_news_crawler.py)
+ [demo_manual_news_crawler.py](examples/demo_manual_news_crawler.py)

## Quickstart

### Automatically Detecting URLs

[demo_auto_news_crawler.py](examples/demo_auto_news_crawler.py):

```python
# coding=utf-8
import webcollector as wc


class NewsCrawler(wc.RamCrawler):
    def __init__(self):
        super().__init__(auto_detect=True)
        self.num_threads = 10
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
```

### Manually Detecting URLs

[demo_manual_news_crawler.py](examples/demo_manual_news_crawler.py):

```python
# coding=utf-8
import webcollector as wc


class NewsCrawler(wc.RamCrawler):
    def __init__(self):
        super().__init__(auto_detect=False)
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
```

### Filter Detected URLs by detected_filter Plugin

[demo_detected_filter.py](examples/demo_detected_filter.py):

```python
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
```