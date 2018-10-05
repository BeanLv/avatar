import ujson

from blueprints.rests import rests
from exceptions import RuntimeException

from dao.biz import BizDAO
from dao.operator import OperatorDAO


@rests.route('/operators/<int:operatorid>/bizs')
def operatorbizs(operatorid):
    try:
        operator = OperatorDAO.first_or_default(id=operatorid, disabled=0)
        if operator is None:
            return '供应商不存在', 404

        bizs = BizDAO.all('updated_at', operator=operatorid, disabled=0)
        for biz in bizs:
            biz.pop('disabled')

        return ujson.dumps({'operatorname': operator['name'],
                            'bizs': bizs})

    except Exception as e:
        raise RuntimeException('获取供应商套餐异常',
                               extra={'operatorid': operatorid}) \
            from e
