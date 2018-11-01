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

    def __init__(self, url):
        self.waf_set = set()
        self.url = auto_assign(url)
        self.th_executor = ThreadExecutor(self.detect)
        for i in range(WafConfig.WAF_PAYLOADS_NUM):
            payload = adjust_url_format(self.url) + random.choice(WafConfig.PAYLOADS_LIST)
            print(payload)
            self.th_executor.push(payload)
        self.loaded_plugins = ScriptQueue(
            WafConfig.WAF_PLUGINS_DIRECTORY, WafConfig.WAF_PLUGINS_IMPORT_TEMPLATE, verbose=False
        ).load_scripts()

    def get_waf_info(self):

        if not is_url_alive(self.url):
            return None

        self.th_executor.run()
        return self.waf_set


    def detect(self, url_with_payload):
        # temp = []
        qstring, status, html, headers = get_page(url_with_payload)
        for detection in self.loaded_plugins:
            if detection.detect(str(html), status=status, headers=headers) is True:
                # temp.append(detection.__product__)
                # if detection.__product__ == lib.settings.UNKNOWN_FIREWALL_NAME and len(temp) == 1:
                #     logging.warning("unknown firewall detected saving fingerprint to log file")
                #     path = lib.settings.create_fingerprint(url, html, status, headers)
                #     return lib.firewall_found.request_firewall_issue_creation(path)
                # else:
                self.waf_set.add(detection.__product__)
                # print(detection.__product__)



