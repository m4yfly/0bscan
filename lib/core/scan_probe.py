#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/15 9:51 PM
# @Author  : zer0i3
# @File    : scan_probe.py
from lib.utils.plugin_util import ScriptQueue
import os
from config import ScanConfig
from lib.utils.net_util import adjust_url_format


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

        for pluginObj in ScanProbe._scan_modules:
            pluginObj.security_note = self._security_note
            pluginObj.security_info = self._security_info
            pluginObj.security_warning = self._security_warning
            pluginObj.security_hole = self._security_hole

    @staticmethod
    def gen_scan_payloads(site_job):
        payloads_list = []
        for plugin_obj in ScanProbe._scan_modules:
            pluginObj_tuple = plugin_obj.assign("www", adjust_url_format(url))
            if not isinstance(pluginObj_tuple, tuple):  # 判断是否是元组
                continue
            else:
                print(pluginObj_tuple, plugin_obj)


    @staticmethod
    def detect(url_job_que):
        pass
