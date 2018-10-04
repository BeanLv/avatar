# -*- coding: UTF-8 -*-

import flask

operations = flask.Blueprint('operations', __name__, url_prefix='/operations')


@operations.route('/healthcheck')
def health_check():
    """ Health check api """
    return '系统正在运行'
