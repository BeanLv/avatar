import flask

from unittest.mock import Mock


def test_close_resource_after_request(app):
    with app.test_request_context():
        obj = Mock(close=Mock())
        flask.g.setdefault('dummpycloseable', obj)

    obj.close.assert_called_once()


def test_unclosed_resource_outside_flaskg(app):
    with app.test_request_context():
        obj = Mock(close=Mock())

    obj.close.assert_not_called()
