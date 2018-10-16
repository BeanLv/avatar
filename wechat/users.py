# -*- coding: UTF-8 -*-

import requests

import wechat
from config import config
from constant import WechatAPP
from exceptions import RuntimeException


def get_users_details():
    addressbook_config = config['apps']['addressbook']
    resp = requests.get(addressbook_config['apiurl'],
                        params={'access_token': wechat.get_app_token(WechatAPP.BACKEND),
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


def get_userid_from_code(code: str) -> str:
    wechat_config = config['wechat']
    access_token = wechat.get_app_token(WechatAPP.BACKEND)

    url = wechat_config['userinfourl']
    params = {'access_token': access_token, 'code': code}

    resp = requests.get(url=url, params=params)

    if resp.status_code != 200:
        raise RuntimeException('发送请求获取用户信息返回!200',
                               extra={'token': access_token,
                                      'code': code,
                                      'resp': resp.text})

    body = resp.json()

    if body.get('errcode', 0) != 0:
        raise RuntimeException('调用API获取用户信息返回错误',
                               extra={'token': access_token,
                                      'code': code,
                                      'errcode': body.get('errcode'),
                                      'errmsg': body.get('errmsg')})

    return body.get('UserId')


def get_taged_users(tagid: int) -> list:
    resp = requests.get(config['wechat']['tagurl'],
                        params={'access_token': wechat.get_app_token(WechatAPP.BACKEND),
                                'tagid': tagid})

    if resp.status_code != 200:
        raise RuntimeException('发送请求获取标签用户返回!200',
                               extra={'tagid': tagid})

    body = resp.json()

    if body.get('errcode', 0) != 0:
        raise RuntimeException('调用API获取标签用户返回错误',
                               extra={'errcode': body.get('errcode'),
                                      'errmsg': body.get('errmsg')})

    return body['userlist']
