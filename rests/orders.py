# -*- coding: UTF-8 -*-

import datetime

import ujson
import flask
import requests

import wechat
from config import config

from blueprints.rests import rests
from exceptions import RuntimeException
from models import OrderStatus, OrderOperation
from models.model_binder import SearchOrderModelBinder, OrderModelBinder
from dao import transaction
from dao.order_view import OrderView
from dao.order import OrderDAO
from dao.order_record import OrderRecordDAO
from dao.biz import BizDAO
from utils import datatime_utils


@rests.route('/orders')
@SearchOrderModelBinder()
def searchorders(pagenum: int = 1, pagesize: int = 20, **kwargs):
    try:
        return ujson.dumps(OrderView.search(pagenum=pagenum,
                                            pagesize=pagesize,
                                            **kwargs))

    except Exception as e:
        raise RuntimeException('搜索订单异常',
                               extra={'pagenum': pagenum,
                                      'pagesize': pagesize,
                                      **kwargs}) \
            from e


@rests.route('/orders', methods=['POST'])
@OrderModelBinder()
def createorder(**kwargs):
    installtime = datetime.datetime.strptime(kwargs.get('installtime'), '%Y-%m-%d %H:%M')
    installtime = datatime_utils.utctime(installtime)
    installtime = installtime.strftime('%Y-%m-%d %H:%M')

    try:
        with transaction():
            # 添加记录
            orderid = OrderDAO.insert({'biz': kwargs.get('biz'),
                                       'status': OrderStatus.WAITING.value,
                                       'realname': kwargs.get('realname'),
                                       'nickname': kwargs.get('nickname'),
                                       'headimgurl': kwargs.get('headimgurl'),
                                       'mobile': kwargs.get('mobile'),
                                       'address': kwargs.get('address'),
                                       'lon': kwargs.get('lon'),
                                       'lat': kwargs.get('lat'),
                                       'installtime': installtime,
                                       'source': kwargs.get('source')})

            OrderRecordDAO.insert({'orderid': orderid,
                                   'operation': OrderOperation.value,
                                   'opname': kwargs.get('realname')})

            # 构造消息
            serverconfig = config['server']

            urltemplate = '{protocal}://{domain}:{port}/pages/order?orderid={orderid}'
            url = urltemplate.format(protocal=serverconfig['protocal'],
                                     domain=serverconfig['domain'],
                                     port=serverconfig['port'],
                                     orderid=orderid)

            msgtemplate = "<div class='gray'>{time}</div><br>" \
                          "<div class='normal'>{bizname}</div><br>" \
                          "<div class='highlight'>{realname} {mobile} {address}</div>"
            msg = msgtemplate.format(realname=kwargs.get('realname'),
                                     mobile=kwargs.get('mobile'),
                                     address=kwargs.get('address'),
                                     bizname=kwargs.get('bizname'),
                                     time=datatime_utils.localtime(datetime.datetime.utcnow()).strftime(
                                         '%Y年%m月%d日 %H:%M:%S'))

            # 发送通知
            token = wechat.get_app_token('order')

            resp = requests.post(config['wechat']['notifyurl'],
                                 params={'access_token': token},
                                 json={'touser': '@all',
                                       'msgtype': 'textcard',
                                       'agentid': config['apps']['order']['agentid'],
                                       'textcard': {
                                           'title': '新订单通知',
                                           'description': msg,
                                           'url': url,
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

            return str(orderid), 201

    except Exception as e:
        raise RuntimeException('提交订单异常', extra={**kwargs}) from e


@rests.route('/orders/<int:orderid>')
def orderdetail(orderid: int):
    try:
        order = OrderDAO.first_or_default(id=orderid)

        if order is None:
            return flask.make_response(('订单不存在', 404))

        order['bizname'] = BizDAO.first_or_default(id=order['biz'])['name']
        order['records'] = OrderRecordDAO.all('created_at', orderid=orderid)

        return ujson.dumps(order)

    except Exception as e:
        raise RuntimeException('获取订单详情异常',
                               extra={'orderid': orderid}) \
            from e
