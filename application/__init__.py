# -*- coding: UTF-8 -*-

import logging

import flask

from config import config
from application import blueprint

logger = logging.getLogger(__name__)

app = flask.Flask(__name__)

app.config.update(config)

# 替换 jinja 模版引擎中的变量运算符，因为这回和 vue 中的绑定表达式冲突 {{ }}
jinja_options = app.jinja_options.copy()
jinja_options.update({'variable_start_string': '{$',
                      'variable_end_string': '$}'})
app.jinja_options = jinja_options

# 注册蓝图，其它模块通过对应的蓝图注册路由
app.register_blueprint(blueprint.pages)
app.register_blueprint(blueprint.rests)
app.register_blueprint(blueprint.ops)


# 请求结束后检查 flask.g 中的可 close 对象，将它们关闭
@app.teardown_appcontext
def close_resource_after_request(err):
    for o in flask.g.__dict__.values():
        if hasattr(o, 'close'):
            try:
                o.close()
            except Exception:
                logger.exception('关闭资源异常: %s' % o.__class__.__name__)
            else:
                logger.debug('关闭资源: %s' % o.__class__.__name__)
