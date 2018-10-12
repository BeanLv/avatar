# -*- coding: UTF-8 -*-

import itertools

import dao
from dao.base_dao import BaseDAO


class PageViewDAO(BaseDAO):
    table = 'pageview'
    columns = ['id', 'date', 'num', 'source']

    @classmethod
    def insert(cls, record: dict):
        sql = "INSERT INTO {TABLE} ({P}) VALUES ({V}) " \
              "ON DUPLICATE KEY UPDATE " \
              "`num`=`num`+VALUES(`num`)".format(TABLE=cls.table,
                                                 P=','.join(record.keys()),
                                                 V=','.join(itertools.repeat('%s', times=len(record))))
        arguments = tuple(record.values())

        connection = dao.connect()
        cursor = connection.cursor()
        cursor.execute(sql, arguments)
        cursor.execute('SELECT LAST_INSERT_ID()')
        createdid = cursor.fetchone()[0]
        connection.commit()

        return createdid
