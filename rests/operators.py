import re

import ujson

from blueprints.rests import rests
from exceptions import RuntimeException
from models.model_binder import RequestParameterBinder
from dao.operator import OperatorDAO


@rests.route('/operators')
def operators():
    try:
        operators = OperatorDAO.all('updated_at', disabled=0)

        for operator in operators:
            operator.pop('disabled')

        return ujson.dumps(operators)

    except Exception as e:
        raise RuntimeException('获取供应商列表异常') \
            from e


@rests.route('/operators', methods=['POST'])
@RequestParameterBinder(name='name', from_json=True, exp=re.compile(r"^\S{1,10}$"), msg='运营商名称为1到10个非空字符')
def createoperator(name: str = None):
    try:
        operatorid = OperatorDAO.insert({'name': name})
        return ujson.dumps({'id': operatorid,
                            'name': name}), \
               201
    except Exception as e:
        raise RuntimeException('创建供应商异常',
                               extra={'name': name}) \
            from e


@rests.route('/operators/<int:operatorid>', methods=['DELETE'])
def deleteoperator(operatorid):
    try:
        OperatorDAO.update({'disabled': 1}, id=operatorid)
        return '', 204
    except Exception as e:
        raise RuntimeException('删除供应商异常',
                               extra={'operatorid': operatorid}) \
            from e


@rests.route('/operators/<int:operatorid>', methods=['PATCH'])
@RequestParameterBinder(name='name', from_json=True, exp=re.compile(r"^\S{1,10}$"), msg='运营商名称为1到10个非空字符')
def updateoperator(operatorid, name: str = None):
    try:
        OperatorDAO.update({'name': name}, id=operatorid)
        return '', 204
    except Exception as e:
        raise RuntimeException('更新供应商名称异常',
                               extra={'operatorid': operatorid,
                                      'name': name}) \
            from e
