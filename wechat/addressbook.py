# -*- coding: UTF-8 -*-

import ujson
import requests

import wechat

from clients import redis
from exceptions import RuntimeException

ADDRESSBOOK_CACHE_KEY = 'ADDRESSBOOK'


def get_user_addressbok(userid: str) -> dict:
    try:
        client = redis.client()
        cacheval = client.hget(ADDRESSBOOK_CACHE_KEY, userid)
        return ujson.decode(cacheval) if cacheval else None
    except Exception as e:
        raise RuntimeException('获取用户通讯异常', extra={'userid': userid}) from e


def setup_cache():
    try:
        token = wechat.get_app_token('addressbook')
        pass


    except Exception as e:
        raise RuntimeException('初始化通讯录缓存异常') from e
