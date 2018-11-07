#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 6:16 PM
# @Author  : zer0i3
# @File    : cms_probe
from lib.utils.net_util import adjust_url_format, get_page
from config import GlobalConfig
import os
import json
import logging
from lib.utils import get_md5
import re


class CMSProbe(object):

    _cms_modules = {}

    @staticmethod
    def load_plugins():
        cms_file = os.path.join(GlobalConfig.BASE_DIR, 'plugins/cms/cms.json')
        with open(cms_file) as f:
            cms_list = json.loads(f.read())
            for cl in cms_list:
                path = cl['path']
                if path not in CMSProbe._cms_modules:
                    CMSProbe._cms_modules[path] = []
                CMSProbe._cms_modules[path].append(cl)
        logging.info("load CMSProbe module success")

    @staticmethod
    def gen_cms_payloads():
        return CMSProbe._cms_modules.keys()

    @staticmethod
    def detect(url_job_que, url):
        cms_list = []
        if not url_job_que.empty():
            payload = url_job_que.get()
            url_with_payload = url + payload
            qstring, status, html, headers = get_page(url_with_payload)
            if status == 200:
                for cp in CMSProbe._cms_modules[payload]:
                    option = cp['option']
                    content = cp['content']
                    cms_name = cp['cms_name']
                    fingter = False
                    if option != 'md5' and not isinstance(html, str):
                        coding='utf-8'
                        if 'custom_encoding' in headers:
                            coding = headers['custom_encoding']
                        html = html.decode(coding)
                    if option == 'md5':
                        if isinstance(html, str):
                            html = html.encode('utf-8')
                        if content == get_md5(html):
                            fingter = True
                    elif option == 'regx':
                        r = re.search(content, html)
                        if r:
                            fingter = True
                    elif option == 'keyword':
                        if content in html:
                            fingter = True
                    if fingter:
                        cms_list.append(cms_name)
        return cms_list

