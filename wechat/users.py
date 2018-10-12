# -*- coding: UTF-8 -*-

import requests

import wechat
from config import config

from exceptions import RuntimeException


def get_users_details():
    try:
        addressbook_config = config['apps']['addressbook']
        token = wechat.get_app_token('backend')
        resp = requests.get(addressbook_config['apiurl'],
                            params={'access_token': token,
                                    'department_id': addressbook_config['deptid']})

        if resp.status_code != 200:
            raise RuntimeException('发送请求获取员工详情返回!200',
                                   extra={'resp': resp.text})

        body = resp.json()

        if body['errcode'] != 0:
            raise RuntimeException('调用API获取员工详情返回错误',
                                   extra={'errcode': body['errcode'],
                                          'errmsg': body['errmsg']})

        return list(filter(lambda u: u['status'] == 1, body['userlist']))

    except Exception as e:
        raise RuntimeException('调用API获取通讯异常') from e
