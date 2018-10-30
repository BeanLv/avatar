# -*- coding: UTF-8 -*-

import logging

import flask

from redis.client import Redis
from redis.connection import ConnectionPool

from config import config

logger = logging.getLogger(__name__)


class RedisClient(Redis):
    """Redis client, 使用一个全局的连接池"""

    _pool = ConnectionPool(**config['redis'])

    def __init__(self, **kwargs):
        kwargs.setdefault('connection_pool', self._pool)
        super().__init__(**kwargs)


def client() -> Redis:
    return RedisClient()
