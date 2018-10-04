import ujson

from blueprints.rests import rests
from exceptions import RuntimeException

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
