# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 11:03 PM
# @Author  : zer0i3
# @File    : job.py
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


class ScriptQueue(object):

    """
    This is where we will load all the scripts that we need to identify the firewall
    or to identify the possible bypass
    """

    def __init__(self, files_path, import_path, verbose=False):
        self.files = files_path
        self.path = import_path
        self.verbose = verbose
        self.skip_schema = ("__init__.py", ".pyc", "__")
        self.script_type = ''.join(self.path.split(".")[1].split())[:-1]

    def load_scripts(self):
        retval = []
        file_list = [f for f in os.listdir(self.files) if not any(s in f for s in self.skip_schema)]
        for script in sorted(file_list):
            script = script[:-3]
            if self.verbose:
                logging.info("loading {} script '{}'".format(self.script_type, script))
            script = importlib.import_module(self.path.format(script))
            retval.append(script)
        return retval