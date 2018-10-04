import pytest
from unittest import mock
from unittest.mock import Mock

import dao


@pytest.fixture(name='connect', autouse=True)
def mock_pymsql_connection_connect_method():
    with mock.patch('pymysql.connections.Connection.connect') as m:
        yield m


@pytest.fixture(name='close', autouse=True)
def mock_dao_connection_close_method():
    with mock.patch('dao.Connection.close') as m:
        yield m


def test_connect(connect, close, app):
    with app.test_request_context():
        connection1 = dao.connect()
        connection2 = dao.connect()
        assert connection1 == connection2

    connect.assert_called_once()
    close.assert_called_once()


@mock.patch('dao.connect')
def test_transaction(connect):
    connection = Mock(spec=dao.Connection)
    connect.return_value = connection

    with dao.transaction():
        pass

    connect.assert_called_once()
    connection.begin.assert_called_once()
    connection.committrans.assert_called_once()
    connection.rollback.assert_not_called()


@mock.patch('dao.connect')
def test_transaction_exception(connect):
    connection = Mock(spec=dao.Connection)
    connect.return_value = connection

    with pytest.raises(ValueError):
        with dao.transaction():
            raise ValueError

    connect.assert_called_once()
    connection.begin.assert_called_once()
    connection.committrans.assert_not_called()
    connection.rollback.assert_called_once()
