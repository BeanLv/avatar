# -*- coding: UTF-8 -*-

# -*- coding: UTF-8 -*-

import logging
from functools import wraps

from config import config
from clients import redis

from constant import CacheKey

logger = logging.getLogger(__name__)


class SetupJob:
    def __init__(self, name: str, envs: list = ('production', 'development'), mark: bool = True):
        self.name = name
        self.envs = envs
        self.mark = mark

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info('SetupJob %s: envs: %s, mark: %s ',
                        self.name, self.envs, self.mark)

            if self.envs and config.get('ENV') not in self.envs:
                logger.info('SetupJob: %s: %s 不在指定环境中，跳过', self.name, config.get('ENVIRONMENT'))
                return

            if self.mark and redis.client().sismember(CacheKey.setupjobs, self.name):
                logger.info('SetupJob: %s: 已经被标记在缓存中，跳过', self.name)
                return

            func(*args, **kwargs)

            if self.mark:
                redis.client().sadd(CacheKey.setupjobs, self.name)

            logger.info('SetupJob: %s: 执行完毕', self.name)

        return wrapper


from . import users
from . import taged_users

setupjobs = [users.setup_users_details_cache,
             taged_users.setup_taged_users_cache]
