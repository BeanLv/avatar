# -*- coding: UTF-8 -*-

import logging

import flask

from services import auth as authservice
from services import users as userservice
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


# @rests.before_request
# def require_login_first():
#     """ 在处理请求前检查用户是否还在登录状态，如果不在的话则返回 401，如果在的话把 userid 设置到上下文中 """
#     try:
#         userid = authservice.get_authed_userid()
#
#         if not userid:
#             return '登录超时', 401
#
#         userservice.set_context_userid(userid=userid)
#
#     except Exception:
#         logger.exception('处理请求前，检查用户登录时异常')
#         return '系统错误，请联系管理员', 500


# import 使用到 blueprint 的模块，在模块中使用 blueprint 注册路由
__import__('rests')
