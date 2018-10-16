# -*- coding: UTF-8 -*-

import logging

import ujson
import flask

from blueprints.rests import rests
from exceptions import RuntimeException
from models import UserTag
from models.model_binder import SearchOrderModelBinder
from dao.order_view import OrderView
from dao.order import OrderDAO
from dao.order_record import OrderRecordDAO
from dao.biz import BizDAO
from dao.operator import OperatorDAO
from dao.qrcode import QrCodeDAO
from services import users as userservice

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
        order = OrderDAO.first_or_default(id=orderid)

        if order is None:
            return flask.make_response(('订单不存在', 404))

        biz = BizDAO.first_or_default(id=order['biz'])
        if biz is None:
            logger.warning('订单没有对应的套餐. order=%s, biz=%s', orderid, order['biz'])
            return '订单状态异常', 412

        operator = OperatorDAO.first_or_default(id=biz['operator'])
        if operator is None:
            logger.warning('订单没有对应的供应商. order=%s, biz=%s, operator=%d', orderid, order['biz'], biz['operator'])
            return '订单状态异常', 412

        order['bizname'] = biz['name']
        order['opname'] = operator['name']
        order['records'] = OrderRecordDAO.all('created_at', orderid=orderid)

        # 根据 source 和 userid 来判断当前用户可执行的操作，添加到返回 header 中
        # 管理员可以派发订单也可以自己接单，二维码来源的订单可以由二维码的负责人接单
        userid = userservice.get_context_userid()
        ordermanagers = userservice.get_taged_usersids(tagname=UserTag.ORDERMANAGER.name)
        order['ismanager'] = userid in ordermanagers

        source = order.get('source')
        if source:
            qrcode = QrCodeDAO.first_or_default(id=source)
            if not qrcode:
                logger.warning('订单的二维码来源不存在. order=%s, source=%s', orderid, source)
                qrcode['isowner'] = False
            else:
                qrcode['isowner'] = qrcode['owner'] == userid

        return ujson.dumps(order)

    except Exception as e:
        raise RuntimeException('获取订单详情异常',
                               extra={'orderid': orderid}) \
            from e
