# -*- coding: UTF-8 -*-

import logging

import flask
from flask import Blueprint

from config import config
from exceptions import RuntimeException, BusinessException

logger = logging.getLogger(__name__)

pages = Blueprint('publicpages', __name__,
                  template_folder='templates',
                  url_prefix='/public/pages')

rests = Blueprint('publicrests', __name__,
                  url_prefix='/public/rests')

static = Blueprint('public', __name__,
                   static_folder=config['public']['staticfolder'],
                   static_url_path='/static',
                   url_prefix='/public')

# 默认的 page 路由
@pages.route('<page>')
def render_page(page):
    return flask.render_template('%s.html' % page)


@rests.errorhandler(RuntimeException)
def handle_runtime_exception(ex):
    logger.exception('接口错误')
    return '接口错误', 500


@rests.errorhandler(BusinessException)
def handle_business_exception(ex):
    logger.exception('业务处理异常')
    return ex.msg, ex.errcode


# 验证 api 权限
rest_api_key = config['server']['apikey']


def check_api_key():
    if flask.request.headers.get('apikey') != rest_api_key:
        flask.abort(flask.make_response(('没有权限', 403)))


if rest_api_key:
    rests.before_request(check_api_key)

# 导入路由
from . import bizs
from . import qrcodes
from . import orders
