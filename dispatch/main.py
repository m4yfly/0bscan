# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 10:53 PM
# @Author  : zer0i3
# @File    : main.py
from dispatch import PQUE
from lib.model import Job
from config import WafConfig, GlobalConfig
from lib.core.waf_probe import WafProbe
import logging
import logging.handlers
import os


def gen_job(url_list):
    for url in url_list:
        PQUE.put(Job(url))


def handle_job(job):
    waf_info = None

    if WafConfig.WAF_DETECT:
        waf_probe = WafProbe(job.url)
        waf_info = waf_probe.get_waf_info()

    if waf_info and WafConfig.WAF_SITE_SKIP:
        return



def schedule():
    while True:
        if not PQUE.empty():
            job = PQUE.get()
            handle_job(job)


def init_logs():
    logger_root = logging.getLogger()
    logger_root.setLevel(logging.INFO)

    log_dir = GlobalConfig.LOG_FOLDER
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    root_log = os.path.join(log_dir, 'root.log')
    if not os.path.exists(root_log):
        open(root_log, 'a').close()

    root_log_handler = logging.handlers.RotatingFileHandler(root_log, maxBytes=100000)
    console_log_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    root_log_handler.setFormatter(formatter)
    console_log_handler.setFormatter(formatter)

    logger_root.addHandler(root_log_handler)
    logger_root.addHandler(console_log_handler)

    logger_root.propagate = 1

    logging.info("Init logs succeed!")


def main():

    init_logs()

    logging.info("---------------------Starting 0bscan----------------------------")

    url_list = ["http://cyberpeace.cn/",'www.baidu2333fsds.com']

    gen_job(url_list)

    schedule()