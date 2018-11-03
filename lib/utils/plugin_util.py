# -*- coding: utf-8 -*-
# @Time    : 2018/11/3 12:13 PM
# @Author  : zer0i3
# @File    : plugin_util.py
#load plugins
import importlib
import logging
import os

class ScriptQueue(object):

    def __init__(self, files_path, import_path):
        self.files = files_path
        self.path = import_path
        self.skip_schema = ("__init__.py", ".pyc", "__")

    def load_scripts(self):
        retval = []
        file_list = [f for f in os.listdir(self.files) if not any(s in f for s in self.skip_schema)]
        for script in sorted(file_list):
            script = script[:-3]
            script = importlib.import_module(self.path.format(script))
            logging.info("load module {} success".format(script))
            retval.append(script)
        return retval