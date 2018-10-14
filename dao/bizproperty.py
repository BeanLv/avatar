# -*- coding: UTF-8 -*-

import dao
from dao.base_dao import BaseDAO

from pymysql.cursors import DictCursor


class BizPropertyDAO(BaseDAO):
    columns = ['id', 'biz', 'name', 'value', 'tag']
    table = 'biz_property'

    @classmethod
    def get_properties_of_bizs(cls, bizids):
        sql = 'SELECT {COLUMNS} ' \
              'FROM {TABLE} ' \
              'WHERE biz IN ({IN}) ' \
              'ORDER BY biz, seq'.format(COLUMNS=','.join(cls.columns),
                                         TABLE=cls.table,
                                         IN=','.join(
                                             [str(b) for b in bizids]))

        connection = dao.connect()
        cursor = connection.cursor(cursor=DictCursor)
        cursor.execute(sql)
        properties = cursor.fetchall()
        cursor.close()

        return properties
