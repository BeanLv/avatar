# -*- coding: UTF-8 -*-

import datetime


def utcstrtime(localstrtime: str):
    """把字符串表示的本地时间转化为UTC表示的时间"""
    install_time = datetime.datetime.strptime(localstrtime, '%Y-%m-%d %H:%M')
    install_time = install_time - datetime.timedelta(hours=8)
    return install_time.strftime('%Y-%m-%d %H:%M')
