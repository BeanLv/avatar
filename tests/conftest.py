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


@pytest.fixture(name='enter_request_context')
def enter_test_request_context(app):
    """
    在依赖到 flask 请求上下文的测试用例中，可以使用该 fixture 进入上下文以访问上下文资源，
    比如 flask.g， flask.current_app 和 flask.request 等。 尤其是 dao.connect 等
    方法创建对象时是基于 request context 的，所有必须依赖上下文。
    如果不想让整个 test method 都处于上下文，(比如需要测试上下文结束后的情况)，则可以手动
    写 with app.test_request_context() 来控制上下文范围
    """
    with app.test_request_context():
        yield
