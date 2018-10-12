# -*- coding: UTF-8 -*-

import logging

from clients import redis
from config import config
from constant import CacheKey
from wechat import users as wechatusers
from services import users as userservice

logger = logging.getLogger(__name__)


def setup_users_details_cache():
    try:
        logger.info('开始加载用户缓存')

        redis_client = redis.client()

        if config.get('TESTING', False):
            logger.info('测试环境，不建用户缓存')
            return

        if config['ENV'] != 'production':
            if redis_client.exists(CacheKey.userdetails):
                logger.info('开发环境，缓存已经存在，不建用户缓存')
                return
            else:
                logger.info('开发环境，用户缓存不存在，建用户缓存')
        else:
            logger.info('生产环境，建用户缓存')

        userdetails = wechatusers.get_users_details()

        if len(userdetails) == 0:
            logger.warning('用户数量为0')
        else:
            logger.info('用户数量为 %d', len(userdetails))

        userservice.set_users_details(userdetails)

        logger.info('加载用户缓存完毕')

    except Exception:
        logger.exception('加载用户缓存异常')
