# -*- coding: UTF-8 -*-

import ujson

from blueprints.rests import rests
from exceptions import RuntimeException
from models.model_binder import BizModelBinder

from dao import transaction
from dao.biz import BizDAO
from dao.bizproperty import BizPropertyDAO


@rests.route('/bizs/<int:bizid>', methods=['GET'])
def getbiz(bizid):
    try:
        biz = BizDAO.first_or_default(id=bizid)

        if not biz:
            return '套餐不存在', 404

        biz['properties'] = BizPropertyDAO.all('id', biz=bizid)
        return ujson.dumps(biz)

    except Exception as e:
        raise RuntimeException('获取套餐详情异常',
                               extra={'bizid': bizid}) \
            from e


@rests.route('/bizs', methods=['POST'])
@BizModelBinder()
def createbiz(name: str = None, operator: int = None, remark: str = None, properties: list = list()):
    try:
        with transaction():
            bizid = BizDAO.insert({'operator': operator, 'name': name, 'remark': remark})
            property_columns = ['biz', 'name', 'value']
            property_rows = [[bizid, p['name'], p['value']] for p in properties]
            BizPropertyDAO.batch_insert(property_columns, property_rows)
            return str(bizid), 201

    except Exception as e:
        raise RuntimeException('创建套餐异常',
                               extra={'name': name,
                                      'operator': operator,
                                      'remark': remark,
                                      'properties': ujson.dumps(properties)}) \
            from e


@rests.route('/bizs/<int:bizid>', methods=['PATCH'])
@BizModelBinder()
def updatebiz(bizid, name: str = None, operator: int = None, remark: str = None, properties: list = list()):
    try:
        with transaction():
            BizDAO.update({'name': name, 'operator': operator, 'remark': remark}, id=bizid)
            property_columns = ['biz', 'name', 'value']
            property_rows = [[bizid, p['name'], p['value']] for p in properties]
            duplicates = ['value']
            BizPropertyDAO.batch_insert_or_update(property_columns, property_rows, duplicates)
            return '', 204

    except Exception as e:
        raise RuntimeException('修改套餐异常',
                               extra={'bizid': bizid,
                                      'name': name,
                                      'operator': operator,
                                      'remark': remark,
                                      'properties': ujson.dumps(properties)}) \
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
