import logging

import pytest

import pymysql

from config import config

logger = logging.getLogger(__name__)


@pytest.fixture(name='pymsqlconnection', scope='session')
def pymysql_connection_fixture(request):
    """原生的 pymsql 连接，用于构造测试数据。每次测试会话只提供一个，结束后关闭。"""
    connection = pymysql.connect(**config['mysql'])
    request.addfinalizer(finalizer=connection.close)
    yield connection
