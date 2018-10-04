import ujson

from blueprints.rests import rests
from exceptions import RuntimeException

from dao.order_statistic_view import OrderStatisticView
from dao.pageview_statistic_view import PageviewStatisticView


@rests.route('/statistics/pageview')
def get_pageview_statistic():
    try:
        return ujson.dumps(PageviewStatisticView.get_statistic())
    except Exception:
        raise RuntimeException('获取页面访问统计异常')


@rests.route('/statistics/order')
def get_order_statistic():
    try:
        return ujson.dumps(OrderStatisticView.get_statistic())
    except Exception:
        raise RuntimeException('获取订单统计异常')
