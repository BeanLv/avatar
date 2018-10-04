# -*- coding: UTF-8 -*-

import logging

import flask

from config import config

from blueprints.pages import pages
from blueprints.rests import rests
from blueprints.operations import operations

logger = logging.getLogger(__name__)

app = flask.Flask(__name__)

# 更新配置
app.config.update(config)

# 替换 jinja 模版引擎中的变量运算符，因为这会和 vue 中的绑定表达式 {{ }} 冲突
jinja_options = app.jinja_options.copy()
jinja_options.update({'variable_start_string': '{$',
                      'variable_end_string': '$}'})
app.jinja_options = jinja_options

# 注册蓝图
app.register_blueprint(pages)
app.register_blueprint(rests)
app.register_blueprint(operations)


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
