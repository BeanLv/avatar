# -*- coding: UTF-8 -*-

import flask
from urllib import parse

from config import config
from clients import redis
from constant import CacheKey


def set_userid(userid: str, expires_in: int):
    """ 设置登录用户的ID """
    flask.session['userid'] = userid
    redis.client().setex(CacheKey.userid(userid=userid), userid, expires_in)


def get_userid() -> str:
    """ 获取登录用户的 ID """
    userid = flask.session.get('userid')

    # 检查 redis 中是否缓存 userid，如果没有，即使session中有也算是登录过期
    if userid:
        if not redis.client().exists(CacheKey.userid(userid=userid)):
            flask.session.pop('userid')
            userid = None

    return userid


def get_login_url(source: str = None):
    """获取跳转登录授权页面的url，采用企业微信登录，跳转链接中添加 source 来源，说明由哪个页面进入登录的，以便在登录成功后跳转回去"""
    server_config = config['server']
    wechat_config = config['wechat']

    redirect_uri_fmt = '{protocal}://{domain}:{port}/{wechatblueprint}{route}?source={source}'
    redirect_uri = redirect_uri_fmt.format(protocal=server_config['protocal'],
                                           domain=server_config['domain'],
                                           port=server_config['port'],
                                           wechatblueprint=wechat_config['blueprintname'],
                                           route=wechat_config['loginredirect'],
                                           source=source)

    query = {'appid': wechat_config['corpid'],
             'redirect_uri': redirect_uri,
             'response_type': 'code',
             'scope': 'snsapi_base'}

    return '{endpoint}?{query_string}#wechat_redirect' \
        .format(endpoint=wechat_config['loginurl'],
                query_string=parse.urlencode(query))
