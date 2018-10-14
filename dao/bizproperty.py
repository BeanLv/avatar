# -*- coding: UTF-8 -*-

from dao.base_dao import BaseDAO


class BizPropertyDAO(BaseDAO):
    columns = ['id', 'biz', 'name', 'value', 'tag']
    table = 'biz_property'
