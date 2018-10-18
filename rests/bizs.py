# -*- coding: UTF-8 -*-

from blueprints.rests import rests
from exceptions import RuntimeException
from models.model_binder import BizModelBinder

from dao import transaction
from dao.biz import BizDAO


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
