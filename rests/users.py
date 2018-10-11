# -*- coding: UTF-8 -*-

import ujson

from blueprints.rests import rests
from exceptions import RuntimeException

from services import users as userservice


@rests.route('/users')
def getuserlist():
    try:
        return ujson.dumps(userservice.get_users_details())
    except Exception as e:
        raise RuntimeException('获取用户详情列表异常') from e
