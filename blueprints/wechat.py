# -*- coding: UTF-8 -*-

import logging

import flask
from flask import Blueprint

from config import config
from wechat import users as wechatusers
from services import auth as authservice

logger = logging.getLogger(__name__)

wechat_config = config['wechat']

blueprint = Blueprint(name=wechat_config['blueprintname'],
                      import_name=__name__,
                      url_prefix='/' + wechat_config['blueprintname'])


@blueprint.route(wechat_config['loginredirect'])
def login():
    try:
        code = flask.request.args.get('code')
        userid = wechatusers.get_userid_from_code(code)

        if not userid:
            return flask.render_template('unauthorized.html')

        authservice.set_authed_userid(userid=userid)

        return flask.redirect(flask.request.args.get('source'))

    except Exception:
        logger.exception('微信登录授权后返回页面处理异常')
        return flask.render_template('500.html'), 500
