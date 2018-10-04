from dao.base_dao import BaseDAO


class OrderRecordDAO(BaseDAO):
    columns = ['id', 'orderid', 'operation', 'opname', 'remark', 'created_at']
    table = 'order_record'
