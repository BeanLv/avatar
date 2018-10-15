# -*- coding: UTF-8 -*-

import logging

import flask
from jinja2 import TemplateNotFound

from services import auth as authservice

logger = logging.getLogger(__name__)

pages = flask.Blueprint('pages', __name__, url_prefix='/pages')


@pages.route('/<page>')
def render_templage(page):
    """ 请求 html 页面的统一入口，/pages/<page> 除非特殊情况，不需要为每个视图单独注册路由 """
    try:
        return flask.render_template('%s.html' % page)

    except TemplateNotFound:
        return flask.render_template('404.html'), 404

    except Exception:
        logger.exception('访问页面异常. %s', flask.request.url)
        return flask.render_template('500.html'), 500


@pages.before_request
def before_render_page():
    try:
        if not authservice.get_userid():
            source = flask.request.url
            loginurl = authservice.get_login_url(source)
            return flask.redirect(loginurl)

    except Exception:
        logger.exception('访问页面前，检查用户登录异常. %s', flask.request.url)
        return flask.render_template('500.html'), 500
