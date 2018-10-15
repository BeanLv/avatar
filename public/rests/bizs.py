# -*- coding: UTF-8 -*-

import logging

import ujson

from blueprints.public.rests import rests
from dao.operator import OperatorDAO
from dao.biz import BizDAO

logger = logging.getLogger(__name__)


@rests.route('/bizs', methods=['GET'])
def bizs():
    try:
        operators = OperatorDAO.all('id', disabled=0)
        bizs = BizDAO.get_bizs_of_operators([o['id'] for o in operators])

        operatordict = {o['id']: o for o in operators}

        for o in operators:
            o['bizs'] = []
            o.pop('id')
            o.pop('disabled')

        for b in bizs:
            operatordict[b['operator']]['bizs'].append(b)
            b.pop('disabled')
            b.pop('operator')

        return ujson.dumps(operators)

    except Exception:
        logger.exception('获取套餐列表异常')
        return '接口错误', 500
