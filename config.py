# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 9:22 AM
# @Author  : zer0i3
# @File    : config.py
import os


class GlobalConfig(object):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    LOG_FOLDER = os.environ.get('LOG_FOLDER') or os.path.join(BASE_DIR, 'logs')

    THREAD_NUM = 16


class WafConfig(object):

    PAYLOADS_LIST = [
        "<frameset><frame src=\"javascript:alert('XSS');\"></frameset>",
        " AND 1=1 ORDERBY(1,2,3,4,5) --;",
        "><script>alert(\"testing\");</script>",
        " AND 1=1 UNION ALL SELECT 1,NULL,1,'<script>alert(\"666\")</script>',table_name FROM information_schema.tables WHERE 2>1--/**/; EXEC xp_cmdshell('cat ../../../etc/passwd')#",
        "<img src=\"javascript:alert(\'XSS\');\">",
        "'))) AND 1=1,SELECT * FROM information_schema.tables ((('",
        "' )) AND 1=1 (( ' -- rgzd",
        ";SELECT * FROM information_schema.tables WHERE 2>1 AND 1=1 OR 2=2 -- qdEf '",
        "' OR '1'=1 '\"",
        "') OR \"a\"=\"a --",
        "<scri<script>pt>alert('123');</scri</script>pt>",
        ";CAT1_GALLERY_1 UNION ALL SELECT (SELECT CAST(CHAR(114)+CHAR(51)+CHAR(100)+CHAR(109)+CHAR(48)+CHAR(118)+CHAR(51)+CHAR(95)+CHAR(104)+CHAR(118)+CHAR(106)+CHAR(95)+CHAR(105)+CHAR(110)+CHAR(106)+CHAR(101)+CHAR(99)+CHAR(116)+CHAR(105)+CHAR(111)+CHAR(110) AS NVARCHAR(4000))),NULL--"
    ]

    #how many payloads try
    WAF_PAYLOADS_NUM = 3

    #waf site skip
    WAF_SITE_SKIP = True

    WAF_PLUGINS_DIRECTORY = "{}/plugins/waf".format(GlobalConfig.BASE_DIR)

    WAF_PLUGINS_IMPORT_TEMPLATE = "plugins.waf.{}"


class NetConfig(object):

    #random user agent switch
    RANDOM_USER_AGENT = True


    #req frequency limit(minimum time interval) s, 0 is no limit
    MINIMUM_TIME_INTERVAL = 0

    #retry num when can't reach
    RETRY_NUM = 1

    #timeout
    TIMEOUT_LIMIT = 15


class HTTP_HEADER:
    """
    HTTP request headers list, putting it in a class because
    it's just easier to grab them then to retype them over
    and over again
    """
    ACCEPT = "Accept"
    ACCEPT_CHARSET = "Accept-Charset"
    ACCEPT_ENCODING = "Accept-Encoding"
    ACCEPT_LANGUAGE = "Accept-Language"
    AUTHORIZATION = "Authorization"
    CACHE_CONTROL = "Cache-Control"
    CONNECTION = "Connection"
    CONTENT_ENCODING = "Content-Encoding"
    CONTENT_LENGTH = "Content-Length"
    CONTENT_RANGE = "Content-Range"
    CONTENT_TYPE = "Content-Type"
    COOKIE = "Cookie"
    EXPIRES = "Expires"
    HOST = "Host"
    IF_MODIFIED_SINCE = "If-Modified-Since"
    LAST_MODIFIED = "Last-Modified"
    LOCATION = "Location"
    PRAGMA = "Pragma"
    PROXY_AUTHORIZATION = "Proxy-Authorization"
    PROXY_CONNECTION = "Proxy-Connection"
    RANGE = "Range"
    REFERER = "Referer"
    REFRESH = "Refresh"
    SERVER = "Server"
    SET_COOKIE = "Set-Cookie"
    TRANSFER_ENCODING = "Transfer-Encoding"
    URI = "URI"
    USER_AGENT = "User-Agent"
    VIA = "Via"
    X_CACHE = "X-Cache"
    X_POWERED_BY = "X-Powered-By"
    X_DATA_ORIGIN = "X-Data-Origin"
    X_FRAME_OPT = "X-Frame-Options"
    X_FORWARDED_FOR = "X-Forwarded-For"
    X_SERVER = "X-Server"
    X_BACKSIDE_TRANS = "X-Backside-Transport"