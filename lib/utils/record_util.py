#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/16 5:29 PM
# @Author  : zer0i3
# @File    : record_util.py
import logging
logger_result = logging.getLogger('result')

def _security_note(self, body, k=''):
    logger_result.info(body + ":" + self.url)


def _security_info(self, body, k=''):
    logger_result.info(body + ":" + self.url)


def _security_warning(self, body, k=''):
    logger_result.warning(body + ":" + self.url)


def _security_hole(self, body, k=''):
    logger_result.error(body + ":" + self.url)