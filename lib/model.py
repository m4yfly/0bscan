# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 9:27 AM
# @Author  : zer0i3
# @File    : model.py
import importlib
import logging
import os
from enum import Enum, unique
import queue
from config import WafConfig
from lib.utils.net_util import auto_assign, is_url_alive, adjust_url_format, get_page
import random
import threading
from lib.core.waf_probe import WafProbe
from config import NetConfig
import time


class JobList(object):

    def __init__(self):
        self.jobs = []
        self.url_req_control = {}
        self.lock = threading.Lock()

    def append(self, item):
        self.jobs.append(item)

    def remove(self, item):
        self.jobs.remove(item)

    def sort(self, *args, **kwargs):
        self.jobs.sort(*args, **kwargs)

    def __len__(self):
        return len(self.jobs)

    def __iter__(self):
        return iter(self.jobs)

    def can_access(self, job):
        with self.lock:
            if job.url not in self.url_req_control.keys():
                self.url_req_control[job.url] = time.time()
                return True
            else:
                now = time.time()
                if now - self.url_req_control[job.url] > NetConfig.MINIMUM_TIME_INTERVAL:
                    self.url_req_control[job.url] = time.time()
                    return True


class JobLevel(object):
    low = 100
    mid = 50
    high = 1

@unique
class JobState(Enum):

    ready = 1
    waf_detect = 2
    end = 3

    def __new__(cls, value):
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __int__(self):
        return self.value

class SiteJob(object):

    def __init__(self, url, priority = JobLevel.low, job_state = JobState.ready):
        self.url = auto_assign(url)
        self.priority = priority
        self.job_state = job_state
        self.url_job_que = queue.Queue()
        self.waf_set = set()
        self.lock = threading.Lock()

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return "<SiteJob> with url:{}".format(self.url)

    def handle(self):

        if self.url_job_que.empty():
            self.change_state()

        self.handle_state()


    def change_state(self):

        #gen payloads and switch to waf state
        if self.job_state == JobState.ready:
            for pl in WafProbe.gen_waf_payloads(self.url):
                self.url_job_que.put(pl)

        self.lock.acquire()
        self.job_state = JobState(int(self.job_state) + 1)
        self.lock.release()

    def handle_state(self):

        #handle waf payloads
        if self.job_state == JobState.waf_detect:
            for wl in WafProbe.detect(self.url_job_que):
                self.waf_set.add(wl)


