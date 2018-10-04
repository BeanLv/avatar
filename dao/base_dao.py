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
    def _where(cls, **where):
        sql_where = 'WHERE ' + ' AND '.join(['{}=%s'.format(n) for n in where.keys()]) if where else ''
        arguments = tuple(where.values()) if where else ()
        return sql_where, arguments

    @classmethod
    def _orderby(cls, *orderby):
        return 'ORDER BY ' + ','.join(orderby) if orderby else ''
