# -*- coding: UTF-8 -*-

import dao
from models import OrderStatus


class OrderView:
    properties = ['id', 'headimgurl', 'bizname', 'status', 'address', 'realname', 'mobile']

    sql_select = "SELECT " \
                 "o.id, " \
                 "o.headimgurl, " \
                 "b.name as bizname, " \
                 "o.status, " \
                 "o.address, " \
                 "o.realname, " \
                 "o.mobile " \
                 "FROM `order` o JOIN `biz` b ON o.biz=b.id " \
                 "{WHERE} " \
                 "ORDER BY o.updated_at DESC, o.status ASC, o.id DESC " \
                 "LIMIT {LIMIT} OFFSET {OFFSET}"

    @classmethod
    def search(cls, pagenum: int = 1, pagesize: int = 20, **kwargs) -> dict:

        ret = {'orders': [], 'total': 0, 'pagenum': pagenum, 'pagesize': pagesize, 'pagecount': 0}

        filters, arguments = [], []

        status = kwargs.get('status')
        if isinstance(status, OrderStatus):
            filters.append('o.status=%s')
            arguments.append(status.value)

        handler = kwargs.get('handler')
        if handler and isinstance(handler, str):
            filters.append('o.handler=%s')
            arguments.append(handler)

        source = kwargs.get('source')
        if isinstance(source, int):
            filters.append('o.source=%s')
            arguments.append(source)

        where = ('WHERE ' + ' AND '.join(filters)) if filters else ''

        connection = dao.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(1) FROM `order` o {WHERE}".format(WHERE=where), arguments)

        ret['total'] = cursor.fetchone()[0]
        if ret['total'] == 0:
            ret['pagenum'] = 1
            cursor.close()
            return ret

        ret['pagecount'] = (ret['total'] + pagesize - 1) // pagesize
        if pagenum > ret['pagecount']:
            pagenum = ret['pagenum'] = ret['pagecount']

        sql = cls.sql_select.format(WHERE=where,
                                    LIMIT=pagesize,
                                    OFFSET=(pagenum - 1) * pagesize)

        cursor.execute(sql, arguments)

        ret['orders'] = [dict(zip(cls.properties, o)) for o in cursor.fetchall()]

        cursor.close()

        return ret
