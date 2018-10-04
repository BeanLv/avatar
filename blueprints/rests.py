# -*- coding: UTF-8 -*-

import logging

import flask

from exceptions import RuntimeException, BusinessException

logger = logging.getLogger(__name__)

rests = flask.Blueprint('rests', __name__, url_prefix='/rests')


@rests.errorhandler(RuntimeException)
def handle_runtime_exception(ex):
    logger.exception('接口错误')
    return '接口错误', 500


@rests.errorhandler(BusinessException)
def handle_business_exception(ex):
    logger.exception('业务处理异常')
    return ex.msg, ex.errcode


# import 使用到 blueprint 的模块，在模块中使用 blueprint 注册路由
__import__('rests')
