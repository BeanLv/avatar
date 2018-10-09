# -*- coding: UTF-8 -*-

from dao.base_dao import BaseDAO


class OperatorDAO(BaseDAO):
    table = 'operator'
    columns = ['id', 'name', 'disabled']
