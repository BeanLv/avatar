import ujson

from blueprints.rests import rests
from exceptions import RuntimeException
from models import OrderStatus
from models.model_binder import SearchOrderModelBinder

from dao.order_view import OrderView


@rests.route('/orders')
@SearchOrderModelBinder()
def orders(status: OrderStatus = None, pagenum: int = 1, pagesize: int = 20):
    try:
        return ujson.dumps(OrderView.searchlist(status=status,
                                                pagenum=pagenum,
                                                pagesize=pagesize))
    except Exception as e:
        raise RuntimeException('搜索订单异常',
                               extra={'status': status,
                                      'pagenum': pagenum,
                                      'pagesize': pagesize}) \
            from e
