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
    def searchlist(cls, status: OrderStatus = None, pagenum: int = 1, pagesize: int = 20) -> dict:
        ret = {'orders': [], 'total': 0, 'pagenum': pagenum, 'pagesize': pagesize, 'pagecount': 0}
        where = cls._where(status=status)
        connection = dao.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(1) FROM `order` o %s" % where)
        ret['total'] = cursor.fetchone()[0]
        if ret['total'] == 0:
            ret['pagenum'] = 1
            return ret

        ret['pagecount'] = (ret['total'] + pagesize - 1) // pagesize
        if pagenum > ret['pagecount']:
            pagenum = ret['pagenum'] = ret['pagecount']

        cursor.execute(cls.sql_select.format(WHERE=where,
                                             LIMIT=pagesize,
                                             OFFSET=(pagenum - 1) * pagesize))

        ret['orders'] = [dict(zip(cls.properties, o)) for o in cursor.fetchall()]

        cursor.close()

        return ret

    @classmethod
    def _where(cls, status: OrderStatus = None):
        return 'WHERE o.status = %d' % status.value if status else ''
