# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 10:53 PM
# @Author  : zer0i3
# @File    : main.py
from dispatch import JOB_LIST
from dispatch.thread_executor import ThreadExecutor
from lib.model import SiteJob, JobState
from config import WafConfig, GlobalConfig, NetConfig
from lib.core.waf_probe import WafProbe
import logging
import logging.handlers
import os
import threading
import time


def gen_job(url_list):
    for url in url_list:
        JOB_LIST.append(SiteJob(url))


def handle_site_job(site_job):
    logging.info("handle site job {}".format(site_job))
    site_job.handle()
    if site_job.job_state == JobState.end:
        logging.info("Job end with url {}, waf_set is {}".format(site_job.url, site_job.waf_set))
        JOB_LIST.remove(site_job)


def handle_job_list():
    for job in JOB_LIST:
        if JOB_LIST.can_access(job):
            handle_site_job(job)
            return


def handle_job():
    while len(JOB_LIST) > 0:
        handle_job_list()


def schedule():
    th = []
    for i in range(GlobalConfig.THREAD_NUM):
        t = threading.Thread(target=handle_job)
        t.start()
        th.append(t)

    for tt in th:
        tt.join()


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

    #remove default handler
    logger_root.removeHandler(logger_root.handlers[0])

    logger_root.propagate = 0

    logging.info("Init logs succeed!")


def main():

    init_logs()

    logging.info("---------------------Starting 0bscan----------------------------")

    url_list = []
    for i in range(2):
        url_list.append("http://www.{}.com".format(i))

    gen_job(url_list)

    schedule()