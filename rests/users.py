# -*- coding: UTF-8 -*-

import ujson

from blueprints.rests import rests
from clients import redis
from exceptions import RuntimeException
from constant import CacheKey


@rests.route('/users')
def getuserlist():
    try:
        client = redis.client()
        userlist = [ujson.loads(o.decode('UTF-8')) for o in client.hvals(CacheKey.userdetail)]
        return ujson.dumps(userlist)
    except Exception as e:
        raise RuntimeException('获取用户列表异常') from e
