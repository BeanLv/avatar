# -*- coding: UTF-8 -*-

import dao
from dao.base_dao import BaseDAO


class OrderDAO(BaseDAO):
    columns = ['id', 'status', 'biz', 'realname', 'nickname', 'headimgurl', 'mobile',
               'address', 'lon', 'lat', 'installtime']
    table = "`order`"

    @classmethod
    def count(cls, **kwargs):
        filters, arguments = [], []

        for p in ['handler', 'source']:
            v = kwargs.get(p)
            if v:
                filters.append('{}=%s'.format(p))
                arguments.append(v)

        startdate = kwargs.get('startdate')
        if startdate:
            filters.append('created_at>=%s')
            arguments.append(startdate)

        enddate = kwargs.get('enddate')
        if enddate:
            filters.append('created_at<=%s')
            arguments.append(enddate)

        where = ('WHERE ' + ' AND '.join(filters)) if filters else ''

        sql = 'SELECT COUNT(1) FROM {TABLE} {WHERE}'.format(TABLE=cls.table,
                                                            WHERE=where)

        connection = dao.connect()
        cursor = connection.cursor()
        cursor.execute(sql, arguments)
        num = cursor.fetchone()[0] or 0
        cursor.close()

        return num
