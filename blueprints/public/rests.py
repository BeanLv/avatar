# -*- coding: UTF-8 -*

import logging

import flask
from flask import Blueprint

from config import config
from exceptions import RuntimeException, BusinessException

import public

logger = logging.getLogger(__name__)

rests = Blueprint(name='publicrests',
                  import_name=public.__name__,
                  url_prefix='/public/rests')

# 验证 api 权限
rest_api_key = config['server']['apikey']


def check_api_key():
    if flask.request.headers.get('apikey') != rest_api_key:
        flask.abort(flask.make_response(('没有权限', 403)))


if rest_api_key:
    rests.before_request(check_api_key)


@rests.errorhandler(RuntimeException)
def handle_runtime_exception(ex):
    logger.exception('接口错误')
    return '接口错误', 500


@rests.errorhandler(BusinessException)
def handle_business_exception(ex):
    logger.exception('业务处理异常')
    return ex.msg, ex.errcod


__import__('public.rests')
