# -*- coding: UTF-8 -*-

import requests

from config import config
from clients import redis
from exceptions import RuntimeException

APPTOKEN_CACHE_KEY = 'APPTOKEN_{APP}'


def get_app_token(name: str) -> str:
    try:
        client = redis.client()
        cachekey = APPTOKEN_CACHE_KEY.format(APP=name)
        cacheval = client.get(cachekey)

        if cacheval:
            return cacheval.decode('UTF-8')

        corpid = config['wechat']['corpid']
        secret = config['wechat'][name]

        resp = requests.get(config['wechat']['apptoken'], params={'corpid': corpid,
                                                                  'corpsecret': secret})

        if resp.status_code != 200:
            raise RuntimeException('调用API获取应用TOKEN返回!200',
                                   extra={'name': name,
                                          'corpid': corpid,
                                          'secret': secret,
                                          'resp': resp.text})

        body = resp.json()

        if body['errcode'] != 0:
            raise RuntimeException('调用API获取应用TOKEN微信返回错误',
                                   extra={'name': name,
                                          'corpid': corpid,
                                          'secret': secret,
                                          'errcode': body['errcode'],
                                          'errmsg': body['errmsg']})

        token = body['access_token']

        client.setex(cachekey, token, body['expires_in'])

        return token

    except Exception as e:
        raise RuntimeException('获取应用Token异常', extra={'name': name}) from e
