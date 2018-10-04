# -*- coding: UTF-8 -*-

import flask
from jinja2 import TemplateNotFound

pages = flask.Blueprint('pages', __name__, url_prefix='/pages')


@pages.route('/<page>')
def render_templage(page):
    """ 请求 html 页面的统一入口，/pages/<page> 除非特殊情况，不需要为每个视图单独注册路由 """
    try:
        return flask.render_template('%s.html' % page)
    except TemplateNotFound:
        flask.abort(404)
