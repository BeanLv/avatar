# -*- coding: UTF-8 -*-

import re
from functools import wraps

import ujson
import flask

from config import config
from models import OrderStatus, OrderOperation
from services import users as userservice
from dao.qrcode import QrCodeDAO


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

                value = flask.request.json.get(self.name) if flask.request.data else None
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

            handler = request.args.get('handler')
            handler = handler if handler and isinstance(handler, str) else None

            source = request.args.get('source', '')
            source = int(source) if source.isdigit() else None

            pagenum = request.args.get('pagenum', '1')
            pagenum = int(pagenum) if pagenum.isdigit() else 1
            pagenum = max(1, pagenum)

            pagesize = request.args.get('pagesize', '20')
            pagesize = int(pagesize) if pagesize.isdigit() else 20
            pagesize = min(50, max(20, pagesize))

            kwargs['status'] = status
            kwargs['handler'] = handler
            kwargs['source'] = source
            kwargs['pagenum'] = pagenum
            kwargs['pagesize'] = pagesize

            return func(*args, **kwargs)

        return wrapper


class OrderModelBinder:
    """将订单属性绑定到处理方法的kwargs中，在绑定之前做校验"""

    _properties = {
        'biz': {'type': int},
        'bizname': {'type': str},
        'operatorname': {'type': str},
        'realname': {'type': str, 'exp': re.compile(r"^.{1,10}$"), 'msg': '请输入真实姓名'},
        'nickname': {'type': str},
        'headimgurl': {'type': str},
        'mobile': {'type': str, 'exp': re.compile(r"^\d{11}$"), 'msg': '请输入11位手机号码'},
        'address': {'type': str, 'exp': re.compile(r"^.{1,100}$"), 'msg': '地址最多100个字符'},
        'lon': {'type': float, 'required': False},
        'lat': {'type': float, 'required': False},
        'source': {'type': int, 'required': False},
        'installtime': {'type': str, 'exp': re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"), 'msg': '安装时间为年-月-日 时:分'},
        'remark': {'type': str, 'required': False, 'exp': re.compile(r"^.{1,140}$"), 'msg': '备注不能超过140个字符'}
    }

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not flask.request.is_json:
                return flask.make_response(('请提交JSON格式的报文', 400))

            body = flask.request.json

            for name, restrict in self._properties.items():
                val = body.get(name)

                if val is None and not restrict.get('required', True):
                    continue

                if val is None:
                    return flask.make_response(('%s 必填' % name, 400))

                if not isinstance(val, restrict.get('type')):
                    return flask.make_response(('%s 只能是 %s 类型' % (name, restrict.get('type').__name__), 400))

                if 'exp' in restrict and restrict['exp'].match(val) is None:
                    return flask.make_response((restrict.get('msg'), 400))

                kwargs[name] = val

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
            if remark and (not isinstance(remark, str) or len(remark) > 100):
                return flask.make_response(('备注必填且必须在100个字符内', 400))

            boards = body.get('boards')
            if not isinstance(boards, list):
                return '属性面板不能为空', 400

            boards = ujson.dumps(boards)

            kwargs['name'] = name
            kwargs['operator'] = operator
            kwargs['boards'] = boards
            kwargs['remark'] = remark

            return func(*args, **kwargs)

        return wrapper


class QrCodeModelBinder:
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = flask.request

            if not request.is_json:
                return flask.make_response(('请求body 不是 application/json', 400))

            body = request.json

            name = body.get('name')
            if not name or not isinstance(name, str):
                return flask.make_response(('二维码名称不对', 400))

            owner = body.get('owner')
            if not isinstance(owner, str):
                return flask.make_response(('必须为二维码指定一个用户', 400))

            remark = body.get('remark')
            if remark and (not isinstance(remark, str) or len(remark) > 100):
                return '备注最多100个字符', 400

            kwargs['name'] = name
            kwargs['owner'] = owner
            kwargs['remark'] = remark

            return func(*args, **kwargs)

        return wrapper


class OrderOperationBinder:
    """ 操作订单参数绑定 """

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not flask.request.is_json:
                return '要提交 application/json', 400

            if not flask.request.data:
                return '报文内容不能为空', 400

            json = flask.request.json

            if 'operation' not in json:
                return 'operation 不能为空', 400

            operation = json['operation']

            allowoperations = [OrderOperation.DISPATCH,
                               OrderOperation.DEALWITH,
                               OrderOperation.FINISH,
                               OrderOperation.CLOSE]

            if operation not in [o.value for o in allowoperations]:
                return 'operation 值非法. %s' % operation, 400

            operation = OrderOperation(operation)

            kwargs['operation'] = operation

            if operation == OrderOperation.DISPATCH:
                if 'handler' not in json:
                    return '指派订单时必须选定一个用户', 400

                handler = json.get('handler')

                if not handler or not isinstance(handler, str):
                    return '用户ID不合法'

                handler = userservice.get_user_detail(handler)
                if not handler:
                    return '指定用户不存在', 400

                kwargs['handler'] = handler

            userid = userservice.get_context_userid()
            user = userservice.get_user_detail(userid)

            kwargs['user'] = user

            return func(*args, **kwargs)

        return wrapper


class QrCodeSourceBinder:
    """扫二维码进入相关页面时，调用api或者访问页面，返回二维码来源，如果不是扫码进入，返回配置中的默认值"""

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user, sourcename, sourcemobile = None, None, None

            source = flask.request.args.get('source')
            if source and source.isdigit():
                qrcode = QrCodeDAO.first_or_default(id=int(source))
                if qrcode and qrcode.get('owner'):
                    user = userservice.get_user_detail(qrcode.get('owner'))

            if user:
                sourcename = user['name']
                sourcemobile = user['mobile']

            if not sourcename or not sourcemobile:
                sourcename = config['corp']['manager']['name']
                sourcemobile = config['corp']['manager']['mobile']

            kwargs['sourcename'] = sourcename
            kwargs['sourcemobile'] = sourcemobile

            return func(*args, **kwargs)

        return wrapper
