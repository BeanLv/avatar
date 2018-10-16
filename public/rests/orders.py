# -*- coding: UTF-8 -*-

import logging
import datetime

import requests

import wechat
from config import config
from blueprints.public.rests import rests
from models import OrderStatus, OrderOperation, UserTag
from models.model_binder import OrderModelBinder
from exceptions import RuntimeException
from utils import datatime_utils
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

            # 构造消息
            serverconfig = config['server']

            urltemplate = '{protocal}://{domain}/pages/order?orderid={orderid}'
            url = urltemplate.format(protocal=serverconfig['protocal'],
                                     domain=serverconfig['domain'],
                                     orderid=orderid)

            msgtemplate = "<div class='gray'>{time}</div><br><br>" \
                          "<div class='normal'>{operatorname} {bizname}</div><br>" \
                          "<div class='highlight'>{realname} {mobile} {address}</div>"
            msg = msgtemplate.format(realname=kwargs.get('realname'),
                                     mobile=kwargs.get('mobile'),
                                     address=kwargs.get('address'),
                                     operatorname=kwargs.get('operatorname'),
                                     bizname=kwargs.get('bizname'),
                                     time=datatime_utils.localtime(datetime.datetime.utcnow()).strftime(
                                         '%Y年%m月%d日 %H:%M:%S'))

            # 获取发送通知的对象
            notifyusersids = set(userservice.get_taged_usersids(tagname=UserTag.ORDERMANAGER.name))
            if 'source' in kwargs:
                qrcode = QrCodeDAO.first_or_default(id=kwargs.get('source'))
                if qrcode:
                    notifyusersids.add(qrcode['owner'])

            tousers = '|'.join(notifyusersids)

            # 发送通知
            token = wechat.get_app_token('order')

            resp = requests.post(config['wechat']['notifyurl'],
                                 params={'access_token': token},
                                 json={'touser': tousers,
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
