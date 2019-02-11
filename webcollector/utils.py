# coding=utf-8

import re


def url_matches(url, url_regex):
    if isinstance(url_regex, str):
        return re.fullmatch(url_regex, url) is not None
    else:
        return url_regex.fullmatch(url) is not None


class RegexRule(object):
    def __init__(self):
        self.pos_regexes = []
        self.neg_regexes = []

    def add(self, regex):
        start_char = regex[0]
        if start_char == '+':
            self.add_pos(regex[1:])
        elif start_char == '-':
            self.add_neg(regex[1:])
        else:
            self.add_pos(regex)

    def add_pos(self, pos_regex):
        self.pos_regexes.append(re.compile(pos_regex))

    def add_neg(self, neg_regex):
        self.neg_regexes.append(re.compile(neg_regex))

    # match rule:
    # - must match at least one pos rule
    # - must not match any neg rule
    def matches(self, url):
        for neg_rule in self.neg_regexes:
            if neg_rule.fullmatch(url) is not None:
                return False
        for pos_rule in self.pos_regexes:
            if pos_rule.fullmatch(url) is not None:
                return True
        return False

