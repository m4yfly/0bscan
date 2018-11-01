# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 9:27 AM
# @Author  : zer0i3
# @File    : model.py
import importlib
import logging
import os

LOW_LEVEL = 100
MID_LEVEL = 50
HIGH_LEVEL = 1

class Job(object):

    def __init__(self, url, priority = LOW_LEVEL):
        self.url = url
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return "<Job> with url:{}".format(self.url)


#load plugins
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