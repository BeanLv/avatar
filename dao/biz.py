# -*- coding: UTF-8 -*-

from pymysql.cursors import DictCursor

import dao
from dao.base_dao import BaseDAO


class BizDAO(BaseDAO):
    columns = ['id', 'name', 'operator', 'boards', 'remark', 'disabled']
    table = 'biz'

    @classmethod
    def get_bizs_of_operators(cls, operatorids):
        sql = 'SELECT {COLUMNS} ' \
              'FROM {TABLE} ' \
              'WHERE disabled=0 ' \
              'AND operator IN ({IN}) ORDER BY id'.format(COLUMNS=','.join(cls.columns),
                                                          TABLE=cls.table,
                                                          IN=','.join(
                                                              [str(b) for b in operatorids]))

        connection = dao.connect()
        cursor = connection.cursor(cursor=DictCursor)
        cursor.execute(sql)
        properties = cursor.fetchall()
        cursor.close()

        return properties
