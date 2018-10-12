# -*- coding: UTF-8 -*-

import time
import requests

from config import config
from clients import redis
from exceptions import RuntimeException, BusinessException

from constant import CacheKey


def get_app_token(name: str) -> str:
    try:
        client = redis.client()
        cachekey = CacheKey.apptoken(appname=name)
        cacheval = client.get(cachekey)

        if cacheval:
            return cacheval.decode('UTF-8')

        corpid = config['wechat']['corpid']
        secret = config['wechat'][name]['secret']

        resp = requests.get(config['wechat']['apptoken'], params={'corpid': corpid,
                                                                  'corpsecret': secret})

        if resp.status_code != 200:
            raise RuntimeException('发送请求获取应用TOKEN返回!200',
                                   extra={'name': name,
                                          'corpid': corpid,
                                          'secret': secret,
                                          'resp': resp.text})

        body = resp.json()

        if body['errcode'] != 0:
            raise RuntimeException('调用API获取应用TOKEN返回错误',
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


def get_minprogram_token():
    try:
        client = redis.client()
        cachekey = CacheKey.apptoken(appname='minprogram')
        cacheval = client.get(cachekey)

        if cacheval:
            return cacheval.decode('UTF-8')

        # 调用API, 按照微信文档，这个接口比较繁忙，可能会超时。所以最多重试3次,如果3次
        # 都超时，则抛出一个业务异常，用 204 表示代码正确执行，但是没有返回任何内容

        minprogram_config = config['minprogram']

        for i in range(0, 3):
            resp = requests.get(minprogram_config['tokenurl'],
                                params={'grant_type': 'client_credential',
                                        'appid': minprogram_config['appid'],
                                        'secret': minprogram_config['secret']})

            if resp.status_code != 200:
                raise RuntimeException('发送请求获取小程序TOKEN返回!200',
                                       extra={'resp': resp.text})

            body = resp.json()

            # 小程序调用成功居然没有 errocode 这个标示，
            # 要用 get 来获取，如果没有就是默认成功0
            errcode = body.get('errcode', 0)

            if errcode == 0:
                client.setex(cachekey, body['access_token'], body['expires_in'])
                return body['access_token']
            elif errcode == -1:
                time.sleep(2)
            else:
                raise RuntimeException('调用API获取小程序TOKEN返回错误',
                                       extra={'errcode': body['errcode'],
                                              'errmsg': body['errmsg']})

    except Exception as e:
        raise RuntimeException('获取小程序TOKEN异常') from e

    # 没有异常但也没有return，说明小程序超时
    raise BusinessException(errcode=204, msg='微信小程序服务繁忙')
