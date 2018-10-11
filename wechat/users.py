# -*- coding: UTF-8 -*-

import requests
import ujson
import redis

import wechat
from config import config
from utils import chinese_utils

from exceptions import RuntimeException
from constant import CacheKey


def get_users_details():
    try:
        addressbook_config = config['wechat']['addressbook']
        token = wechat.get_app_token('backend')
        resp = requests.get(addressbook_config['apiurl'],
                            params={'access_token': token,
                                    'department_id': addressbook_config['deptid']})

        if resp.status_code != 200:
            raise RuntimeException('调用API获取员工详情返回!200',
                                   extra={'resp': resp.text})

        body = resp.json()

        if body['errcode'] != 0:
            raise RuntimeException('调用API获取员工详情返回错误',
                                   extra={'errcode': body['errcode'],
                                          'errmsg': body['errmsg']})

        return list(filter(lambda u: u['status'] == 1, body['userlist']))


    except RuntimeException:
        raise
    except Exception as e:
        raise RuntimeException('获取通讯异常') from e


def setup_cache():
    try:

        userdetaillist = [{'id': o['userid'],
                           'name': o['name'],
                           'headimgurl': o['avatar'],
                           'mobile': o['mobile'],
                           'qrcode': o['qr_code'],
                           'isleader': bool(o['isleader']),
                           'pinying': chinese_utils.get_pinying(o['name'])
                           }
                          for o in get_users_details()]

        userdetaildict = {u['id']: ujson.dumps(u) for u in userdetaillist}

        client = redis.Redis(**config['redis'])

        client.hmset(CacheKey.userdetail, userdetaildict)

    except Exception as e:
        raise RuntimeException('创建用户详情缓存异常') from e
