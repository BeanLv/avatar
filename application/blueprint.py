# -*- coding: UTF-8 -*-

import flask
from jinja2 import TemplateNotFound

pages = flask.Blueprint('pages', __name__, url_prefix='/pages')
rests = flask.Blueprint('rests', __name__, url_prefix='/rests')
ops = flask.Blueprint('ops', __name__, url_prefix='/ops')


@pages.route('/<page>')
def render_templage(page):
    """ 请求 html 页面的统一入口，/pages/<page> 除非特殊情况，不需要为每个视图单独注册路由 """
    try:
        return flask.render_template('%s.html' % page)
    except TemplateNotFound:
        flask.abort(404)


@ops.route('/healthcheck')
def health_check():
    """ Health check api """
    return '系统正在运行'


# import 使用到blueprint的模块，在模块中使用blueprint注册路由
__import__('rest')
