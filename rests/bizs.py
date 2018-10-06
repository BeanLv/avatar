import re

from blueprints.rests import rests
from exceptions import RuntimeException
from models.model_binder import RequestParameterBinder

from dao.biz import BizDAO


@rests.route('/bizs/<int:bizid>', methods=['DELETE'])
def deletebiz(bizid):
    try:
        BizDAO.update({'disabled': 1}, id=bizid)
        return '', 204
    except Exception as e:
        raise RuntimeException('删除套餐异常',
                               extra={'bizid': bizid}) \
            from e


@rests.route('/bizs/<int:bizid>', methods=['PATCH'])
@RequestParameterBinder(name='name', from_json=True, exp=re.compile(r"^\S{1,10}$"), msg='套餐名称为1到10个非空字符')
def updatebiz(bizid, name: str = None):
    try:
        BizDAO.update({'name': name}, id=bizid)
        return '', 204
    except Exception as e:
        raise RuntimeException('修改套餐名称异常',
                               extra={'bizid': bizid,
                                      'name': name}) \
            from e
