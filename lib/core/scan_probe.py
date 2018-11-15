#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/15 9:51 PM
# @Author  : zer0i3
# @File    : scan_probe.py
from lib.utils.plugin_util import ScriptQueue
import os
from config import ScanConfig


class ScanProbe(object):

    _scan_modules = []

    @staticmethod
    def load_plugins():
        for plugin in os.listdir(ScanConfig.WAF_PLUGINS_DIRECTORY):
            plugin_path = os.path.join(ScanConfig.WAF_PLUGINS_DIRECTORY, plugin)
            if os.path.isdir(plugin_path):
                loaded = ScriptQueue(
                    plugin_path, ScanConfig.WAF_PLUGINS_IMPORT_TEMPLATE.format(plugin) + ".{}"
                ).load_scripts()
                ScanProbe._scan_modules.extend(loaded)

    @staticmethod
    def gen_waf_payloads(url):
        pass


    @staticmethod
    def detect(url_job_que):
        pass
