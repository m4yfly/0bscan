# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 10:01 PM
# @Author  : zer0i3
# @File    : __init__.py
import hashlib


def get_md5(c):
    m = hashlib.md5()
    m.update(c)
    psw = m.hexdigest()
    return psw
