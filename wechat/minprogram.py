# -*- coding: UTF-8 -*-

import requests

import wechat
from config import config
from exceptions import RuntimeException, BusinessException


def generate_qrcode(qrcodeid: int):
    try:
        minprogram_config = config['minprogram']
        qrcode_config = minprogram_config['qrcode']

        createurl = '{endpoint}?access_token={token}'.format(endpoint=qrcode_config['createurl'],
                                                             token=wechat.get_minprogram_token())

        resp = requests.post(createurl, json={'scene': str(qrcodeid),
                                              'is_hyaline': True})

        if resp.status_code != 200:
            raise RuntimeException('发送请求生产二维码返回!200',
                                   extra={'resp': resp.text})

        if 'application/json' in resp.headers.get('Content-Type'):
            body = resp.json()
            raise RuntimeException('调用API生产二维码返回错误',
                                   extra={'errcode': body['errcode'],
                                          'errmsg': body['errmsg'],
                                          'resp': resp.text})

        return resp.content

    except BusinessException:
        raise
    except Exception as e:
        raise RuntimeException('生成二维码异常',
                               extra={'qrcode': qrcodeid}) \
            from e
