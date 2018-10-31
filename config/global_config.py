# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 11:46 PM
# @Author  : zer0i3
# @File    : global_config.py
import os

class GlobalConfig(object):

    #waf detect switch
    WAF_DETECT = True

    #waf site skip
    WAF_SITE_SKIP = True

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    LOG_FOLDER = os.environ.get('LOG_FOLDER') or os.path.join(BASE_DIR, 'logs')

    WAF_PLUGINS_DIRECTORY = "{}/plugins/waf".format(BASE_DIR)

    WAF_PLUGINS_IMPORT_TEMPLATE = "plugins.waf.{}"