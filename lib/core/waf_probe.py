# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 10:57 PM
# @Author  : zer0i3
# @File    : waf_probe.py
from lib.utils.net_util import adjust_url_format, get_page
from config import WafConfig
import random
import logging
from lib.utils.plugin_util import ScriptQueue


class WafProbe(object):

    _waf_modules = None

    @staticmethod
    def load_plugins():
        WafProbe._waf_modules = ScriptQueue(
                WafConfig.WAF_PLUGINS_DIRECTORY, WafConfig.WAF_PLUGINS_IMPORT_TEMPLATE
            ).load_scripts()

    @staticmethod
    def gen_waf_payloads(url):

        payloads_list = []
        for i in range(WafConfig.WAF_PAYLOADS_NUM):
            payload = adjust_url_format(url) + random.choice(WafConfig.PAYLOADS_LIST)
            logging.info("create payload {} in SiteJob for {}".format(payload, url))
            payloads_list.append(payload)
        return payloads_list

    @staticmethod
    def detect(url_job_que):
        waf_list = []
        if not url_job_que.empty():
            url_with_payload = url_job_que.get()
            qstring, status, html, headers = get_page(url_with_payload)
            for detection in WafProbe._waf_modules:
                if detection.detect(str(html), status=status, headers=headers) is True:
                    waf_list.append(detection.__product__)
        return waf_list



