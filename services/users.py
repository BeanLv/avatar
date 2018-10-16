# -*- coding: UTF-8 -*-

import flask
import ujson

from clients import redis
from constant import CacheKey
from utils import chinese_utils


def get_context_userid():
    """
    获取当前上下文的用户ID, 和 auth 不一样，如果用户在进入请求的时候没有在某个地方获取用户 ID 并设置到这里，就拿不到.
    对应 set_context_userid
    """
    return flask.g.userid if 'userid' in flask.g else None


def set_context_userid(userid: str):
    """
    在用户进入请求的时候通过 auth 获取用户ID，如果获取到则运行请求，并且把用户 ID 设置到请求的上下文中
    对应 get_context_userid
    """
    flask.g.userid = userid


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
