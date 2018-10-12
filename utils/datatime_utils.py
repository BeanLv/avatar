# -*- coding: UTF-8 -*-

import datetime


def utctime(localtime: datetime.datetime):
    return localtime - datetime.timedelta(hours=8)


def localtime(utctime: datetime.datetime):
    return utctime + datetime.timedelta(hours=8)
