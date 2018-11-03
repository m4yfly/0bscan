# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 10:34 PM
# @Author  : zer0i3
# @File    : net_util.py

import random, re
from config import NetConfig
import requests
from requests.exceptions import SSLError,ConnectionError
import logging
from urllib.parse import urlparse
import time
import functools

USER_AGENTS = [
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]


#get user_agent
def get_user_agent():
    if NetConfig.RANDOM_USER_AGENT:
        return random.choice(USER_AGENTS)
    else:
        return USER_AGENTS[-1]

# regex to detect the URL protocol (http or https)
PROTOCOL_DETECTION = re.compile("http(s)?")

# check if a query is in a URL or not
URL_QUERY_REGEX = re.compile(r"(.*)[?|#](.*){1}\=(.*)")

#check https or http
def is_url_alive(url):
    res = get_page(url)
    #response status code
    if res[1] == 0:
        logging.warning("{} is not reachable".format(url))
        return False
    else:
        logging.info("url {} is alive".format(url))
        return True

#check if a protocol is given in the URL if it isn't we'll auto assign it
def auto_assign(url, ssl=False):

    if PROTOCOL_DETECTION.search(url) is None:
        if ssl:
            logging.warning("no protocol discovered, assigning HTTPS (SSL)")
            return "https://{}".format(url.strip())
        else:
            logging.warning("no protocol discovered assigning HTTP")
            return "http://{}".format(url.strip())
    else:
        if ssl:
            logging.info("forcing HTTPS (SSL) connection")
            items = PROTOCOL_DETECTION.split(url)
            item = items[-1].split("://")
            item[0] = "https://"
            return ''.join(item)
        else:
            return url.strip()


# adjust url format to add payload
def adjust_url_format(url):
    if URL_QUERY_REGEX.search(url) is None:
        if url[-1] != '/':
            url = url + '/'
    return url


# get the query parameter out of a URL
def get_query(url):

    data = urlparse(url)
    query = "{}?{}".format(data.path, data.query)
    return query


def raw_get_page(url, **kwargs):
    logging.info("requests for {} with params:{}".format(url, kwargs))
    proxy = kwargs.get("proxy", None)
    agent = kwargs.get("agent", get_user_agent())
    provided_headers = kwargs.get("provided_headers", None)

    req_timeout = kwargs.get("timeout", 15)
    request_method = kwargs.get("request_method", "GET")
    post_data = kwargs.get("post_data", " ")

    if request_method == "POST":
        req = requests.post
    else:
        req = requests.get

    if provided_headers is None:
        headers = {"Connection": "close", "User-Agent": agent}
    else:
        headers = {}
        if type(provided_headers) == dict:
            for key, value in provided_headers.items():
                headers[key] = value
            headers["User-Agent"] = agent
        else:
            headers = provided_headers
            headers["User-Agent"] = agent
    proxies = {} if proxy is None else {"http": proxy, "https": proxy}
    error_retval = ("", 0, "", {})

    try:
        res = req(url, headers=headers, proxies=proxies, timeout=req_timeout, data=post_data)
        coding = res.encoding
        if not coding:
            coding = 'utf-8'
        res_content =  res.content.decode(coding)
        logging.info("respones for {} is {}".format(url, res.status_code))
        return "{} {}".format(request_method, get_query(url)), res.status_code, res_content, res.headers
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        logging.warning("respones for {} use default error_retval".format(url))
        return error_retval


def get_page(url, retry_num=NetConfig.RETRY_NUM , **kwargs):
    res_tuple = raw_get_page(url, ** kwargs)
    count = 0
    while res_tuple == ("", 0, "", {}) and count < retry_num:
        count += 1
        logging.info("Retry with {} count {}".format(url, count))
        res_tuple = raw_get_page(url, **kwargs)
    return res_tuple

