import pytest


@pytest.fixture(autouse=True)
def enter_request_context(app):
    """
    DAO 和 RedisClient 等类型都被标记为 InstancePerHttpRequest,
    它们的创建会依赖于 flask 的 app request context，在这之前需要
    进入一个 request context，否则报错。每一个集成测试方法也是在一个
    请求上下文中完成的
    """
    with app.test_request_context():
        yield
