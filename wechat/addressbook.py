# -*- coding: UTF-8 -*-

import ujson
import requests

import wechat

from clients import redis
from exceptions import RuntimeException

ADDRESSBOOK_CACHE_KEY = 'ADDRESSBOOK'


def get_addressbook():
    try:
        client = redis.client()
        cachevals = client.hvals(ADDRESSBOOK_CACHE_KEY)
        return [ujson.decode(v) for v in cachevals] if cachevals else []
    except Exception as e:
        raise RuntimeException('获取通讯异常') from e


def get_user_addressbok(userid: str) -> dict:
    try:
        client = redis.client()
        cacheval = client.hget(ADDRESSBOOK_CACHE_KEY, userid)
        return ujson.decode(cacheval) if cacheval else None
    except Exception as e:
        raise RuntimeException('获取用户通讯异常', extra={'userid': userid}) from e

