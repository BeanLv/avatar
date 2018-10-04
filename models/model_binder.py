from functools import wraps

import flask

from models import OrderStatus


class SearchOrderModelBinder:
    """将搜索订单的参数绑定到搜索函数的参数中"""

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = flask.request

            status = request.args.get('status', '0')
            status = int(status) if status.isdigit() else 0
            status = OrderStatus(status) if OrderStatus.WAITING.value <= status <= OrderStatus.CLOSED.value else None

            pagenum = request.args.get('pagenum', '1')
            pagenum = int(pagenum) if pagenum.isdigit() else 1
            pagenum = max(1, pagenum)

            pagesize = request.args.get('pagesize', '20')
            pagesize = int(pagesize) if pagesize.isdigit() else 20
            pagesize = min(50, max(20, pagesize))

            kwargs['status'] = status
            kwargs['pagenum'] = pagenum
            kwargs['pagesize'] = pagesize

            return func(*args, **kwargs)

        return wrapper
