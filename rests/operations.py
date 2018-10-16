# -*- coding: UTF-8 -*-

import ujson

from models import OrderOperation, OrderStatus
from models.model_binder import OrderOperationBinder
from utils import order_utils
from dao import transaction
from dao.order import OrderDAO
from dao.order_record import OrderRecordDAO
from services import orders as orderservice

from exceptions import RuntimeException

from blueprints.rests import rests


@rests.route('/orders/<int:orderid>/operations', methods=['POST'])
@OrderOperationBinder()
def operateorder(orderid: int, **kwargs):
    try:
        with transaction():
            order = orderservice.get_orderdetail(orderid)

            if order is None:
                return '订单不存在', 400

            operation = kwargs.get('operation')

            handlers = {OrderOperation.DISPATCH: _dispatchorder,
                        OrderOperation.DEALWITH: _dealwithorder,
                        OrderOperation.FINISH: _finishorder,
                        OrderOperation.CLOSE: _closeorder}

            return handlers[operation](order, **kwargs)

    except Exception as e:
        raise RuntimeException('操作订单异常',
                               extra={'orderid': orderid,
                                      **kwargs}) \
            from e


def _dispatchorder(order, **kwargs):
    if order['status'] != OrderStatus.WAITING.value:
        return '订单状态不能指派', 412

    # 更新状态
    OrderDAO.update({'status': OrderStatus.WORKING.value}, id=order['id'])

    # 添加操作记录
    username = kwargs.get('user')['name']
    handlername = kwargs.get('handler')['name']

    OrderRecordDAO.insert({'orderid': order['id'],
                           'operation': OrderOperation.DISPATCH,
                           'opname': ujson.dumps([username, handlername])})

    # 发送通知
    order_utils.send_order_notify_message(title='%s 给你分了一个订单' % username,
                                          tousers=kwargs.get('handler')['id'],
                                          orderid=order['id'],
                                          realname=order['realname'],
                                          mobile=order['mobile'],
                                          address=order['address'],
                                          operatorname=order['operatorname'],
                                          bizname=order['bizname'])

    return str(OrderStatus.WORKING), 201


def _dealwithorder(order, **kwargs):
    pass


def _finishorder(order, **kwargs):
    pass


def _closeorder(order, **kwargs):
    pass
