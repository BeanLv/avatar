# -*- coding: UTF-8 -*-

import logging

import ujson
import flask

from blueprints.rests import rests
from exceptions import RuntimeException
from models import UserTag
from models.model_binder import SearchOrderModelBinder
from dao.order_view import OrderView
from dao.qrcode import QrCodeDAO
from services import users as userservice
from services import orders as orderservice

logger = logging.getLogger(__name__)


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


@rests.route('/orders/<int:orderid>')
def orderdetail(orderid: int):
    try:
        order = orderservice.get_orderdetail(orderid)

        if order is None:
            return flask.make_response(('订单不存在', 404))

        order['installtime'] = order['installtime'].strftime('%Y-%m-%d %H:%M:00')

        # 根据 source 和 userid 来判断当前用户可执行的操作，添加到返回 header 中
        # 管理员可以派发订单也可以自己接单，二维码来源的订单可以由二维码的负责人接单,
        # 订单负责人和管理员可以完成订单，管理员可以关闭订单
        userid = userservice.get_context_userid()

        # 管理员
        ordermanagers = userservice.get_taged_usersids(tagname=UserTag.ORDERMANAGER.name)
        order['ismanager'] = userid in ordermanagers

        # 处理人
        order['ishandler'] = userid == order['handler']

        if order['handler']:
            handler = userservice.get_user_detail(order['handler'])
            order['handlername'] = handler['name'] if handler else '未知用户'

        # 二维码来源
        source = order.get('source')
        if source:
            qrcode = QrCodeDAO.first_or_default(id=source)
            if not qrcode:
                logger.warning('订单的二维码来源不存在. order=%s, source=%s', orderid, source)
                order['issource'] = False
                order['sourcename'] = None
            else:
                order['issource'] = qrcode['owner'] == userid
                order['sourcename'] = qrcode['name']

        return ujson.dumps(order)

    except Exception as e:
        raise RuntimeException('获取订单详情异常',
                               extra={'orderid': orderid}) \
            from e
