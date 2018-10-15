# -*- coding: UTF-8 -*-

import ujson

from clients import redis
from constant import CacheKey
from utils import chinese_utils


def get_users_details():
    return [ujson.loads(o.decode('UTF-8')) for o in redis.client().hvals(CacheKey.userdetails)]


def get_user_detail(userid: str):
    hval = redis.client().hget(CacheKey.userdetails, userid)
    return ujson.loads(hval.decode('UTF-8')) if hval else None


def set_users_details(usersdetails):
    userdetaillist = [{'id': o['userid'],
                       'name': o['name'],
                       'headimgurl': o['avatar'],
                       'mobile': o['mobile'],
                       'qrcode': o['qr_code'],
                       'isleader': bool(o['isleader']),
                       'pinying': chinese_utils.get_pinying(o['name'])
                       }
                      for o in usersdetails]

    userdetaildict = {u['id']: ujson.dumps(u) for u in userdetaillist}
    redis.client().hmset(CacheKey.userdetails, userdetaildict)


def set_user_detail(userdetail):
    redis.client().hset(CacheKey.userdetails, userdetail['id'], ujson.dumps(userdetail))


def set_taged_usersids(tagname: str, userids: list):
    redis.client().sadd(CacheKey.tagedusers(tagname=tagname), *userids)


def get_taged_usersids(tagname: str):
    cachevals = redis.client().smembers(CacheKey.tagedusers(tagname=tagname))
    return [v.decode('UTF-8') for v in cachevals] if cachevals else []
