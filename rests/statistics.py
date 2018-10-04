import ujson

from blueprints.rests import rests
from exceptions import RuntimeException

from dao.pageview_statistic_view import PageviewStatisticView


@rests.route('/statistics/pageview')
def get_pageview_statistic():
    try:
        return ujson.dumps(PageviewStatisticView.get_statistic())
    except Exception:
        raise RuntimeException('获取页面统计异常')
