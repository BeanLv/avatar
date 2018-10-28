# -*- coding: UTF-8 -*-

import ujson

from blueprints.rests import rests
from exceptions import RuntimeException
from models.model_binder import BizModelBinder

from dao import transaction
from dao.biz import BizDAO
from dao.operator import OperatorDAO


@rests.route('/bizs/<int:bizid>')
def getbiz(bizid):
    try:
        biz = BizDAO.first_or_default(id=bizid)

        if biz is None:
            return '套餐不存在', 404

        operator = OperatorDAO.first_or_default(id=biz['operator'])

        if operator is None:
            return '套餐的供应商%d不存在' % biz['operator'], 404

        biz['operator'] = operator['id']
        biz['operatorname'] = operator['name']
        biz['boards'] = ujson.loads(biz['boards'])

        return ujson.dumps(biz)

    except Exception as e:
        raise RuntimeException('获取套餐详情异常',
                               extra={'bizid': bizid}) \
            from e


@rests.route('/bizs', methods=['POST'])
@BizModelBinder()
def createbiz(**kwargs):
    try:
        with transaction():
            bizid = BizDAO.insert({**kwargs})
            return str(bizid), 201

    except Exception as e:
        raise RuntimeException('创建套餐异常',
                               extra={**kwargs}) \
            from e


@rests.route('/bizs/<int:bizid>', methods=['PATCH'])
@BizModelBinder()
def updatebiz(bizid, **kwargs):
    try:
        with transaction():
            BizDAO.update({**kwargs}, id=bizid)
            return '', 204

    except Exception as e:
        raise RuntimeException('修改套餐异常',
                               extra={'bizid': bizid,
                                      **kwargs}) \
            from e


@rests.route('/bizs/<int:bizid>', methods=['DELETE'])
def deletebiz(bizid):
    try:
        BizDAO.update({'disabled': 1}, id=bizid)
        return '', 204

    except Exception as e:
        raise RuntimeException('删除套餐异常',
                               extra={'bizid': bizid}) \
            from e
