# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 10:53 PM
# @Author  : zer0i3
# @File    : main.py
from dispatch import JOB_LIST
from dispatch.thread_executor import ThreadExecutor
from lib.model import SiteJob, JobState
from config import WafConfig, GlobalConfig, NetConfig
from lib.core.waf_probe import WafProbe
from lib.core.cms_probe import CMSProbe
from lib.core.scan_probe import ScanProbe
import logging
import logging.handlers
import os
import threading
logger_result = logging.getLogger('result')


def gen_job(url_list):
    for url in url_list:
        sj = SiteJob(url)
        if sj.is_alive():
            JOB_LIST.append(sj)


def handle_site_job(site_job):
    if site_job.handle():
        logger_result.info("Job end with url {}, waf_set is {}".format(site_job.url, site_job.waf_set))
        logger_result.info("Job end with url {}, cms_set is {}".format(site_job.url, site_job.cms_set))
        logging.info("Job end with url {}, waf_set is {}".format(site_job.url, site_job.waf_set))
        logging.info("Job end with url {}, cms_set is {}".format(site_job.url, site_job.cms_set))
        JOB_LIST.remove(site_job)


def handle_job_list():
    for job in JOB_LIST:
        if JOB_LIST.can_access(job):
            handle_site_job(job)
            return


def handle_job():
    while not JOB_LIST.is_end():
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
    logger_result.setLevel(logging.INFO)

    log_dir = GlobalConfig.LOG_FOLDER
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    root_log = os.path.join(log_dir, 'root.log')
    if not os.path.exists(root_log):
        open(root_log, 'a').close()

    result_log = os.path.join(log_dir, 'result.log')
    if not os.path.exists(result_log):
        open(result_log, 'a').close()

    root_log_handler = logging.handlers.RotatingFileHandler(root_log, maxBytes=100000)
    result_log_handler = logging.handlers.RotatingFileHandler(result_log, maxBytes=100000)
    console_log_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    root_log_handler.setFormatter(formatter)
    console_log_handler.setFormatter(formatter)
    result_log_handler.setFormatter(formatter)

    # remove default handler
    if len(logger_root.handlers) > 0:
        logger_root.removeHandler(logger_root.handlers[0])

    logger_root.addHandler(root_log_handler)
    logger_root.addHandler(console_log_handler)
    logger_result.addHandler(result_log_handler)

    logger_root.propagate = 0
    logger_result.propagate = 0

    logging.info("Init logs succeed!")


def init_result():
    if not os.path.exists(GlobalConfig.RESULT_FOLDER):
        os.makedirs(GlobalConfig.RESULT_FOLDER)


def load_plugins():
    WafProbe.load_plugins()
    CMSProbe.load_plugins()
    ScanProbe.load_plugins()

def main():

    init_logs()

    init_result()

    logging.info("---------------------Starting 0bscan----------------------------")

    load_plugins()

    url_list = ['http://cyberpeace.cn']
    # for i in range(2):
    #     url_list.append("http://www.{}.com".format(i))

    gen_job(url_list)

    schedule()
