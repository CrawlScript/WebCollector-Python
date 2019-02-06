# coding=utf-8
from webcollector.fetch import Fetcher


class Crawler(object):
    def __init__(self, db_manager, generator):
        self.db_manager = db_manager
        self.generator = generator
        self.fetcher = None
        self.num_threads = 10

    def add_seed(self, seed_or_seeds):
        if isinstance(seed_or_seeds, list):
            seeds = seed_or_seeds
        else:
            seeds = [seed_or_seeds]
        self.db_manager.inject(seeds)

    def execute(self, page, detected):
        pass

    def start_once(self, depth_index):
        self.fetcher = Fetcher(self.db_manager, self.generator)
        self.fetcher.start(self.execute, self.num_threads)

    def start(self, num_depth):
        for depth_index in num_depth:
            self.start_once(depth_index)

