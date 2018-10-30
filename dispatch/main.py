# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 10:53 PM
# @Author  : zer0i3
# @File    : main.py
from dispatch import PQUE
from lib.model import Job


def gen_job(url_list):
    for url in url_list:
        PQUE.put(Job(url))

def schedule():
    while True:
        if not PQUE.empty():
            job = PQUE.get()
            print(job)

def main():
    url_list = ["www.baidu.com"]
    gen_job(url_list)
    schedule()