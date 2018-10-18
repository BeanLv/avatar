# -*- coding: UTF-8 -*-

import ujson

from models import OrderOperation, OrderStatus, UserTag
from models.model_binder import OrderOperationBinder
from utils import order_utils
from dao import transaction
from dao.order import OrderDAO
from dao.order_record import OrderRecordDAO
from dao.qrcode import QrCodeDAO
from services import orders as orderservice
from services import users as userservice

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
        return '状态过期，请刷新页面', 412

    user = kwargs.get('user')
    handler = kwargs.get('handler')

    # 更新状态
    OrderDAO.update({'status': OrderStatus.WORKING.value,
                     'handler': kwargs.get('handler')['id']
                     },
                    id=order['id'])

    # 添加操作记录
    OrderRecordDAO.insert({'orderid': order['id'],
                           'operation': OrderOperation.DISPATCH.value,
                           'opname': user['name'] + '|' + handler['name']})

    # 发送通知
    order_utils.send_order_notify_message(title='订单分配通知',
                                          message='%s分了个订单给你' % user['name'],
                                          tousers=kwargs.get('handler')['id'],
                                          orderid=order['id'],
                                          realname=order['realname'],
                                          mobile=order['mobile'],
                                          address=order['address'],
                                          operatorname=order['operatorname'],
                                          bizname=order['bizname'])

    ishandler = user['id'] == handler['id']

    return ujson.dumps({'ishandler': ishandler}), 201


def _dealwithorder(order, **kwargs):
    if order['status'] != OrderStatus.WAITING.value:
        return '状态过期，请刷新页面', 412

    user = kwargs.get('user')

    # 更新状态
    OrderDAO.update({'status': OrderStatus.WORKING.value,
                     'handler': user['id']
                     },
                    id=order['id'])

    # 添加操作记录
    OrderRecordDAO.insert({'orderid': order['id'],
                           'operation': OrderOperation.DEALWITH.value,
                           'opname': user['name']})

    return user['name'], 201


def _finishorder(order, **kwargs):
    if order['status'] != OrderStatus.WORKING.value:
        return '状态过期，请刷新页面', 412

    user = kwargs.get('user')

    # 更新状态
    OrderDAO.update({'status': OrderStatus.DONE.value},
                    id=order['id'])

    # 添加操作记录
    OrderRecordDAO.insert({'orderid': order['id'],
                           'operation': OrderOperation.FINISH.value,
                           'opname': user['name']})

    # 发送通知
    order_utils.send_order_notify_message(title='订单完成通知',
                                          message='%s完成了订单' % user['name'],
                                          tousers=_get_notify_users_when_finish_or_close(order),
                                          orderid=order['id'],
                                          realname=order['realname'],
                                          mobile=order['mobile'],
                                          address=order['address'],
                                          operatorname=order['operatorname'],
                                          bizname=order['bizname'])

    return '', 201


def _closeorder(order, **kwargs):
    if order['status'] in [OrderStatus.DONE.value, OrderStatus.CLOSED.value]:
        return '状态过期，请刷新页面', 412

    user = kwargs.get('user')

    # 更新状态
    OrderDAO.update({'status': OrderStatus.CLOSED.value},
                    id=order['id'])

    # 添加操作记录
    OrderRecordDAO.insert({'orderid': order['id'],
                           'operation': OrderOperation.CLOSE.value,
                           'opname': user['name']})

    # 发送通知
    order_utils.send_order_notify_message(title='订单完成通知',
                                          message='%s关闭了订单' % user['name'],
                                          tousers=_get_notify_users_when_finish_or_close(order),
                                          orderid=order['id'],
                                          realname=order['realname'],
                                          mobile=order['mobile'],
                                          address=order['address'],
                                          operatorname=order['operatorname'],
                                          bizname=order['bizname'])

    return '', 201


def _get_notify_users_when_finish_or_close(order):
    """ 完成或关闭订单时发送通知的对象 """

    # 订单管理员
    managers_ids = userservice.get_taged_usersids(UserTag.ORDERMANAGER.name)
    touserids = set(managers_ids)

    # 二维码来源
    source = order.get('source')
    if source:
        qrcode = QrCodeDAO.first_or_default(id=source)
        if qrcode:
            touserids.add(qrcode['owner'])

    # 订单处理人
    handler = order.get('handler')
    if handler:
        touserids.add(handler)

    return '|'.join(touserids)
