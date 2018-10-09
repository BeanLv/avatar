# -*- coding: UTF-8 -*-

import ujson
import flask

from blueprints.rests import rests
from exceptions import RuntimeException
from models import OrderStatus
from models.model_binder import SearchOrderModelBinder

from dao.order_view import OrderView
from dao.order import OrderDAO
from dao.order_record import OrderRecordDAO
from dao.biz import BizDAO


@rests.route('/orders')
@SearchOrderModelBinder()
def orders(status: OrderStatus = None, pagenum: int = 1, pagesize: int = 20):
    try:
        return ujson.dumps(OrderView.searchlist(status=status,
                                                pagenum=pagenum,
                                                pagesize=pagesize))
    except Exception as e:
        raise RuntimeException('搜索订单异常',
                               extra={'status': status,
                                      'pagenum': pagenum,
                                      'pagesize': pagesize}) \
            from e


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
