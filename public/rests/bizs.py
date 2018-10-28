# -*- coding: UTF-8 -*-

import logging

import ujson

from config import config
from blueprints.public.rests import rests
from dao.operator import OperatorDAO
from dao.biz import BizDAO
from models.model_binder import QrCodeSourceBinder

logger = logging.getLogger(__name__)


@rests.route('/bizs', methods=['GET'])
@QrCodeSourceBinder()
def bizs(sourcename=None, sourcemobile=None):
    try:
        operators = OperatorDAO.all('id', disabled=0)
        bizs = BizDAO.all(disabled=0)

        operatordict = {o['id']: o for o in operators}

        for o in operators:
            o['bizs'] = []
            o.pop('id')
            o.pop('disabled')

        for b in bizs:
            operatordict[b['operator']]['bizs'].append(b)
            b.pop('boards')
            b.pop('disabled')
            b.pop('operator')

        return ujson.dumps({'operators': operators,
                            'source': {'name': sourcename,
                                       'mobile': sourcemobile},
                            'customerservice': {'tel': config['corp']['customer']['tel']}
                            })

    except Exception:
        logger.exception('获取套餐列表异常')
        return '接口错误', 500
