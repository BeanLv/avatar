# -*- coding: UTF-8 -*-

import logging
import datetime

from blueprints.public.rests import rests
from models import OrderStatus, OrderOperation, UserTag
from models.model_binder import OrderModelBinder
from exceptions import RuntimeException
from utils import datatime_utils, order_utils
from dao import transaction
from dao.order import OrderDAO
from dao.order_record import OrderRecordDAO
from dao.qrcode import QrCodeDAO
from services import users as userservice

logger = logging.getLogger(__name__)


@rests.route('/orders', methods=['POST'])
@OrderModelBinder()
def createorder(**kwargs):
    installtime = datetime.datetime.strptime(kwargs.get('installtime'), '%Y-%m-%d %H:%M')
    installtime = datatime_utils.utctime(installtime)
    installtime = installtime.strftime('%Y-%m-%d %H:%M')

    try:
        with transaction():
            # 添加记录
            logger.debug('新增订单: %s', {**kwargs})

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
                                   'operation': OrderOperation.CREATE.value,
                                   'opname': kwargs.get('realname')})

            # 获取发送通知的对象
            notifyusersids = set(userservice.get_taged_usersids(tagname=UserTag.ORDERMANAGER.name))
            if kwargs.get('source'):
                qrcode = QrCodeDAO.first_or_default(id=kwargs.get('source'))
                if qrcode:
                    notifyusersids.add(qrcode['owner'])

            tousers = '|'.join(notifyusersids)

            # 发送通知
            order_utils.send_order_notify_message(title='新订单通知',
                                                  message='有新订单了',
                                                  tousers=tousers,
                                                  orderid=orderid,
                                                  realname=kwargs.get('realname'),
                                                  mobile=kwargs.get('mobile'),
                                                  address=kwargs.get('address'),
                                                  operatorname=kwargs.get('operatorname'),
                                                  bizname=kwargs.get('bizname'))

            return str(orderid), 201

    except Exception as e:
        raise RuntimeException('提交订单异常', extra={**kwargs}) from e
