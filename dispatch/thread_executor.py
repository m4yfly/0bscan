# -*- coding: utf-8 -*-
# @Time    : 2018/10/31 4:07 PM
# @Author  : zer0i3
# @File    : thread_executor.py
import queue
import threading
import logging
import traceback

class ThreadExecutor(object):

    def __init__(self, external_func ,thread_num = 16):
        self.thread_num = 16
        self.que = queue.Queue()
        self.external_func = external_func

    def push(self, task_content):
        self.que.put(task_content)

    def run(self):
        th = []
        for i in range(self.thread_num):
            t = threading.Thread(target=self.execute)
            t.start()
            th.append(t)

        for tt in th:
            tt.join()


    def execute(self):
        while not self.que.empty():
            try:
                task_content = self.que.get()
                self.external_func(task_content)
            except Exception:
                logging.error("error occured in thread_executor with task_content:{}".format(str(task_content)))
                logging.error("detail:" + traceback.format_exc())