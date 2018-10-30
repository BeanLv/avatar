# -*- coding: UTF-8 -*-

import ujson

from exceptions import RuntimeException
from dao.order_record import OrderRecordDAO
from utils import datetime_utils

from blueprints.rests import rests


@rests.route('/orders/<int:orderid>/records')
def get_order_records(orderid: int):
    try:
        records = OrderRecordDAO.all('created_at', orderid=orderid)

        for record in records:
            record['time'] = datetime_utils.strftime(datetime_utils.localtime(record['created_at']))
            record.pop('created_at')

        return ujson.dumps(records)

    except Exception as e:
        raise RuntimeException('获取订单记录异常',
                               extra={'orderid': orderid}) \
            from e
