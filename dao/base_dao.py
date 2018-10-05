import itertools

from pymysql.cursors import DictCursor

import dao


class BaseDAO:
    table = None
    columns = None
    pkid = 'id'

    @classmethod
    def first_or_default(cls, **where):
        sql_where, arguments = cls._where(**where)

        sql = "SELECT {COLUMNS} FROM {TABLE} {WHERE}".format(COLUMNS=','.join(cls.columns),
                                                             TABLE=cls.table,
                                                             WHERE=sql_where)

        connection = dao.connect()
        cursor = connection.cursor(cursor=DictCursor)
        cursor.execute(sql, arguments) if arguments else cursor.execute(sql)

        return cursor.fetchone()

    @classmethod
    def all(cls, *orderby, **where):
        sql_orderby = cls._orderby(*orderby)
        sql_where, arguments = cls._where(**where)

        sql = "SELECT {COLUMNS} FROM {TABLE} {WHERE} {ORDERBY}".format(COLUMNS=','.join(cls.columns),
                                                                       TABLE=cls.table,
                                                                       WHERE=sql_where,
                                                                       ORDERBY=sql_orderby)

        connection = dao.connect()
        cursor = connection.cursor(cursor=DictCursor)
        cursor.execute(sql, arguments) if arguments else cursor.execute(sql)

        return cursor.fetchall()

    @classmethod
    def insert(cls, properties: dict):
        sql = "INSERT INTO {TABLE} ({P}) VALUES ({V})".format(TABLE=cls.table,
                                                              P=','.join(properties.keys()),
                                                              V=','.join(itertools.repeat('%s', times=len(properties))))
        arguments = tuple(properties.values())

        connection = dao.connect()
        cursor = connection.cursor()
        cursor.execute(sql, arguments)
        cursor.execute('SELECT LAST_INSERT_ID()')
        operatorid = cursor.fetchone()
        connection.commit()

        return operatorid

    @classmethod
    def update(cls, properties: dict, **where):
        sql_where, arguments = cls._where(**where)
        arguments = tuple(properties.values()) + arguments

        sql = "UPDATE {TABLE} SET {P} {WHERE}".format(TABLE=cls.table,
                                                      P=','.join(['{}=%s'.format(n) for n in properties.keys()]),
                                                      WHERE=sql_where)

        connection = dao.connect()
        cursor = connection.cursor()
        cursor.execute(sql, arguments)
        connection.commit()

    @classmethod
    def _where(cls, **where):
        sql_where = 'WHERE ' + ' AND '.join(['{}=%s'.format(n) for n in where.keys()]) if where else ''
        arguments = tuple(where.values()) if where else ()
        return sql_where, arguments

    @classmethod
    def _orderby(cls, *orderby):
        return 'ORDER BY ' + ','.join(orderby) if orderby else ''
