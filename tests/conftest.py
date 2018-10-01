# -*- coding: UTF-8 -*-

import os

# 如果在控制台使用原生命令启动测试，配置文件可能不在环境变量中，
# 所以在测试的最最最开始处检查，如果没有设置，则用一个默认的.
os.environ.setdefault('APPCONFIG', 'tests/resources/config.app.yml')

import pytest
from application import app

# 等服务启动起来后再运行后面的所有测试
app.test_client().get('/operations/healthcheck')


@pytest.fixture(name='app', scope='session')
def appfixture():
    """全局 app，如果没有特殊情况，测试用例可以用这个 app"""
    return app


@pytest.fixture(name='appclient', scope='session')
def appclientfixture():
    """全集 appclient ,如果没有特殊情况，测试用例可以用这个 appclient 来发请求"""
    return app.test_client()
