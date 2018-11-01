# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 10:57 PM
# @Author  : zer0i3
# @File    : waf_probe.py
from lib.utils.net_util import auto_assign, is_url_alive, adjust_url_format, get_page
from config import WafConfig
from dispatch.thread_executor import ThreadExecutor
from lib.model import ScriptQueue
import random
import logging



class WafProbe(object):

    _waf_modules = None

    def __init__(self, url):
        self.waf_set = set()
        self.url = auto_assign(url)
        self.th_executor = ThreadExecutor(self.detect)

        if not WafProbe._waf_modules:
            WafProbe._waf_modules = ScriptQueue(
                WafConfig.WAF_PLUGINS_DIRECTORY, WafConfig.WAF_PLUGINS_IMPORT_TEMPLATE
            ).load_scripts()

        for i in range(WafConfig.WAF_PAYLOADS_NUM):
            payload = adjust_url_format(self.url) + random.choice(WafConfig.PAYLOADS_LIST)
            logging.info("create payload {}".format(payload))
            self.th_executor.push(payload)

    def get_waf_info(self):

        if not is_url_alive(self.url):
            return None

        self.th_executor.run()
        logging.info("waf in {} is {}".format(self.url, self.waf_set))
        return self.waf_set


    def detect(self, url_with_payload):

        qstring, status, html, headers = get_page(url_with_payload)
        for detection in WafProbe._waf_modules:
            if detection.detect(str(html), status=status, headers=headers) is True:
                self.waf_set.add(detection.__product__)



