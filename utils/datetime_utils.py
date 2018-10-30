# -*- coding: UTF-8 -*-

import datetime


def utc8now():
    """
    不同服务器的时区可能不一样，datetime.now() 的结果也可能不一样。
    localnow 返回北京时区当前时间。
    """
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)


def localtime(utctime: datetime.datetime) -> datetime.datetime:
    return utctime + datetime.timedelta(hours=8)


def strftime(time: datetime.datetime) -> str:
    return time.strftime('%Y-%m-%d %H:%M:%S')
