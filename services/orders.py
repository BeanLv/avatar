# -*- coding: UTF-8 -*-

import logging

from dao.order import OrderDAO
from dao.biz import BizDAO
from dao.operator import OperatorDAO

logger = logging.getLogger(__name__)


def get_orderdetail(orderid: int):
    order = OrderDAO.first_or_default(id=orderid)

    if order is None:
        return None

    # 套餐
    biz = BizDAO.first_or_default(id=order['biz'])
    if biz is None:
        logger.error('订单没有对应的套餐. order=%s, biz=%s', orderid, order['biz'])
        return None

    order['bizname'] = biz['name']

    # 供应商
    operator = OperatorDAO.first_or_default(id=biz['operator'])
    if operator is None:
        logger.error('订单没有对应的供应商. order=%s, biz=%s, operator=%d', orderid, order['biz'], biz['operator'])
        return None

    order['operatorname'] = operator['name']

    return order
