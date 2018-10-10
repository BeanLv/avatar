# -*- coding: UTF-8 -*-

import ujson

from blueprints.rests import rests

from exceptions import RuntimeException


@rests.route('/users')
def getuserssimplelist():
    try:
        return ujson.dumps([
            {'id': 'caochao', 'name': '曹操', 'headimgurl': 'http://www.sanguosha.com/uploads/201610/580f2ae08104c.jpg'},
            {'id': 'guojia', 'name': '郭嘉', 'headimgurl': 'http://www.sanguosha.com/uploads/201610/580f2fcf4ba5f.jpg'},
            {'id': 'zhangliao', 'name': '张辽',
             'headimgurl': 'http://www.sanguosha.com/uploads/201610/580f2dc2d482f.jpg'}])
    except Exception as e:
        raise RuntimeException('获取用户列表异常') from e
