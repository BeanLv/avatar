# -*- coding: UTF-8 -*-

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
    def insert(cls, record: dict) -> int:
        sql = "INSERT INTO {TABLE} ({P}) VALUES ({V})".format(TABLE=cls.table,
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
    def batch_insert(cls, columns, rows):
        row_values = '(' + ','.join(itertools.repeat('%s', len(columns))) + ')'
        sql_values = ','.join(itertools.repeat(row_values, len(rows)))
        arguments = [v for row in rows for v in row]

        sql = "INSERT INTO {TABLE} ({COLUMNS}) VALUES {VALUES}".format(TABLE=cls.table,
                                                                       COLUMNS=','.join(columns),
                                                                       VALUES=sql_values)
        connection = dao.connect()
        cursor = connection.cursor()
        cursor.execute(sql, arguments)
        connection.commit()
        cursor.close()

    @classmethod
    def batch_insert_or_update(cls, columns, rows, columns_updated_on_duplicate):
        row_values = '(' + ','.join(itertools.repeat('%s', len(columns))) + ')'
        sql_values = ','.join(itertools.repeat(row_values, len(rows)))
        dumpicates = ','.join(['{0}=VALUES({0})'.format(c) for c in columns_updated_on_duplicate])

        sql = "INSERT INTO {TABLE} ({COLUMNS}) VALUES {VALUES} " \
              "ON DUPLICATE KEY UPDATE {DUPLIATES}".format(TABLE=cls.table,
                                                           COLUMNS=','.join(columns),
                                                           VALUES=sql_values,
                                                           DUPLIATES=dumpicates)
        connection = dao.connect()
        cursor = connection.cursor()
        cursor.execute(sql, [v for row in rows for v in row])
        connection.commit()
        cursor.close()

    @classmethod
    def update(cls, record: dict, **where):
        sql_where, arguments = cls._where(**where)
        arguments = tuple(record.values()) + arguments

        sql = "UPDATE {TABLE} SET {P} {WHERE}".format(TABLE=cls.table,
                                                      P=','.join(['{}=%s'.format(n) for n in record.keys()]),
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
