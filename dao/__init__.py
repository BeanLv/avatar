from contextlib import contextmanager

import flask
from pymysql import connections

from config import config


class Connection(connections.Connection):
    """
    pymysql connection 的子类
    提供一个默认游标，如没有特殊情况，一次请求中用一个默认游标就够了
    同时提供一个隐式的事务，在 contextmanager.transaction上下
    文中，dao 提交的一连串 commit 都会被忽略，直到最后才执行。这对
    dao 本身是不可见的，所以它正常实现自己的逻辑，由调用方来确定是否
    需要在一个事务中执行
    """

    def __init__(self, **kwargs):
        self._cursor = None
        self._trans = False
        kwargs.update(config['mysql'])
        super().__init__(**kwargs)

    @property
    def defaultcursor(self):
        if self._cursor is None:
            self._cursor = self.cursor()
        return self._cursor

    def begin(self):
        self._trans = True
        super().begin()

    def commit(self):
        if self._trans:
            super().commit()

    def committrans(self):
        super().commit()
        self._trans = False

    def close(self):
        if self._cursor:
            self._cursor.close()
        super().close()


@contextmanager
def transaction():
    """启动一个事务，此范围内调用的所有commit会被忽略，直到结束的时候才真正的提交 """
    connection = Connection()
    try:
        connection.begin()
        yield
        connection.committrans()
    except:
        connection.rollback()
        raise


def connect() -> Connection:
    return flask.g.get('connection') if 'connection' in flask.g else \
        flask.g.setdefault('connection')
