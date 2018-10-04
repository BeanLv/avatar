from pymysql.cursors import DictCursor

import dao


class BaseDAO:
    table = None
    columns = None
    pkid = 'id'

    @classmethod
    def get_by_id(cls, pkid) -> dict:
        sql = 'SELECT {columns} FROM {table} WHERE id = %s'.format(columns=','.join(cls.columns),
                                                                   table=cls.table)
        connection = dao.connect()
        cursor = connection.cursor(cursor=DictCursor)
        cursor.execute(sql, (pkid,))

        return cursor.fetchone()

    @classmethod
    def get_by_column(cls, column, val) -> dict:
        sql = 'SELECT {columns} FROM {table} WHERE {column} = %s'.format(columns=','.join(cls.columns),
                                                                         table=cls.table,
                                                                         column=column)
        connection = dao.connect()
        cursor = connection.cursor(cursor=DictCursor)
        cursor.execute(sql, (val,))

        return cursor.fetchone()

    @classmethod
    def get_many_by_column(cls, column, val, orderby=None) -> list:
        sql_order = 'ORDER BY %s' if orderby else ''
        sql = 'SELECT {columns} FROM {table} WHERE {column} = %s {orderby}'.format(columns=','.join(cls.columns),
                                                                                   table=cls.table,
                                                                                   column=column,
                                                                                   orderby=sql_order)

        connection = dao.connect()
        cursor = connection.cursor(cursor=DictCursor)
        cursor.execute(sql, (val, orderby)) if orderby else cursor.execute(sql, (val,))

        return cursor.fetchall()
