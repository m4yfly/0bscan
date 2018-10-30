# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 11:03 PM
# @Author  : zer0i3
# @File    : job.py
LOW_LEVEL = 100
MID_LEVEL = 50
HIGH_LEVEL = 1

class Job(object):

    def __init__(self, url, priority = LOW_LEVEL):
        self.url = url
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return "<Job> with url:{}".format(self.url)