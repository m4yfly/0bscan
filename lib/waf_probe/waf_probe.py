# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 10:57 PM
# @Author  : zer0i3
# @File    : waf_probe.py


class WafProbe(object):
    #使用单例模式，避免多次加载
    __instance=None
    def __init__(self):
        probe_payload_list = []

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

