# -*- coding: UTF-8 -*

import datetime

import requests

from constant import WechatAPP
from config import config
from utils import datatime_utils
import wechat

from exceptions import RuntimeException


def get_order_detail_url(orderid: int):
    serverconfig = config['server']

    urltemplate = '{protocal}://{domain}/pages/orderdetail?orderid={orderid}'
    url = urltemplate.format(protocal=serverconfig['protocal'],
                             domain=serverconfig['domain'],
                             orderid=orderid)

    return url


def get_order_message(realname, mobile, address, operatorname, bizname) -> str:
    msgtemplate = "<div class='gray'>{time}</div><br><br>" \
                  "<div class='normal'>{operatorname} {bizname}</div><br>" \
                  "<div class='highlight'>{realname} {mobile} {address}</div>"

    msg = msgtemplate.format(realname=realname,
                             mobile=mobile,
                             address=address,
                             operatorname=operatorname,
                             bizname=bizname,
                             time=datatime_utils.localtime(datetime.datetime.utcnow()).strftime(
                                 '%Y年%m月%d日 %H:%M:%S'))

    return msg


def send_order_notify_message(title, tousers, orderid, realname, mobile, address, operatorname, bizname):
    # 获取发送通知 token
    token = wechat.get_app_token(WechatAPP.ORDER)

    # 构造消息
    msg = get_order_message(realname=realname,
                            mobile=mobile,
                            address=address,
                            operatorname=operatorname,
                            bizname=bizname)

    # 发送通知
    resp = requests.post(config['wechat']['notifyurl'],
                         params={'access_token': token},
                         json={'touser': tousers,
                               'msgtype': 'textcard',
                               'agentid': config['apps'][WechatAPP.ORDER]['agentid'],
                               'textcard': {
                                   'title': title,
                                   'description': msg,
                                   'url': get_order_detail_url(orderid),
                                   'btntxt': '查看详情'
                               }})

    if resp.status_code != 200:
        raise RuntimeException('发送请求发送订单通知返回!200',
                               extra={'resp': resp.text})

    body = resp.json()
    if body.get('errcode', 0) != 0:
        raise RuntimeException('调用API发送通知返回错误',
                               extra={'errcode': body.get('errcode'),
                                      'errmsg': body.get('errmsg')})
