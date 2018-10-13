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

    @classmethod
    def sum(cls, **kwargs):
        filters, arguments = [], []

        for p in ['date', 'source']:
            v = kwargs.get(p)
            if v:
                filters.append('{}=%s'.format(p))
                arguments.append(v)

        startdate = kwargs.get('startdate')
        if startdate:
            filters.append('date>=%s')
            arguments.append(startdate)

        enddate = kwargs.get('enddate')
        if enddate:
            filters.append('date<=%s')
            arguments.append(enddate)

        where = ('WHERE ' + ' AND '.join(filters)) if filters else ''

        sql = 'SELECT SUM(`num`) FROM {TABLE} {WHERE}'.format(TABLE=cls.table,
                                                              WHERE=where)

        connection = dao.connect()
        cursor = connection.cursor()
        cursor.execute(sql, arguments)
        num = cursor.fetchone()[0] or 0
        cursor.close()

        return num
