# coding=utf-8
import logging
import sys

from webcollector.plugin.redis import RedisCrawler
from webcollector.plugin.ram import RamCrawler


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s')
