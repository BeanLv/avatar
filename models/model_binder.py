# -*- coding: UTF-8 -*-

import re
from functools import wraps

import flask

from models import OrderStatus


class RequestParameterBinder:
    """将请求中的参数绑定到执行函数的 kwargs 中"""

    def __init__(self, name, required=True, value_type=str, exp=None, restricts=None, msg=None, from_json=False,
                 constructor=None):
        self.name = name
        self.required = required
        self.value_type = value_type
        self.exp = exp
        self.restricts = restricts
        self.msg = msg
        self.from_json = from_json
        self.constructor = constructor

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.from_json:
                if not flask.request.is_json:
                    return flask.make_response(('请求报文需要为JSON格式', 400))
                value = flask.request.json.get(self.name)
            else:
                value = flask.request.args.get(self.name)

            if value is None:
                return flask.make_response(('%s 必填' % self.name, 400)) if self.required \
                    else func(*args, **kwargs)

            if not isinstance(value, self.value_type):
                return flask.make_response(('%s 应该是 %s' % (self.name, self.value_type.__name__), 400))

            if self.exp and self.exp.match(value) is None:
                return flask.make_response((self.msg or '%s 格式错误' % self.name, 400))

            if self.restricts and value not in self.restricts:
                return flask.make_response(('%s 不在限定范围内' % self.name, 400))

            kwargs[self.name] = self.constructor(value) if self.constructor else value

            return func(*args, **kwargs)

        return wrapper


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


class BizModelBinder:
    """创建套餐参数绑定"""

    name_re = re.compile('^\S{1,10}$')

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = flask.request

            if not request.is_json:
                return flask.make_response(('请求body 不是 application/json', 400))

            body = request.json

            name = body.get('name')
            if not name or not isinstance(name, str) or self.name_re.match(name) is None:
                return flask.make_response(('套餐名称不对', 400))

            operator = body.get('operator')
            if not isinstance(operator, int) or operator < 0:
                return flask.make_response(('供应商不对', 400))

            remark = body.get('remark')
            if not isinstance(remark, str) or len(remark) > 100:
                return flask.make_response(('备注必填且必须在100个字符内', 400))

            properties = body.get('properties')
            if not properties or not isinstance(properties, list):
                return flask.make_response(('缺少属性list', 400))

            kwargs['name'] = name
            kwargs['operator'] = operator
            kwargs['remark'] = remark
            kwargs['properties'] = properties

            return func(*args, **kwargs)

        return wrapper


class QrCodeModelBinder:
    name_re = re.compile('^\S{1,10}$')

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = flask.request

            if not request.is_json:
                return flask.make_response(('请求body 不是 application/json', 400))

            body = request.json

            name = body.get('name')
            if not name or not isinstance(name, str) or self.name_re.match(name) is None:
                return flask.make_response(('二维码名称不对', 400))

            owner = body.get('owner')
            if not isinstance(owner, str):
                return flask.make_response(('必须为二维码指定一个用户', 400))

            remark = body.get('remark')
            if not isinstance(remark, str) or len(remark) > 100:
                return flask.make_response(('备注必填且必须在100个字符内', 400))

            kwargs['name'] = name
            kwargs['owner'] = owner
            kwargs['remark'] = remark

            return func(*args, **kwargs)

        return wrapper
