from dao.base_dao import BaseDAO


class BizPropertyDAO(BaseDAO):
    columns = ['id', 'biz', 'name', 'value', 'seq']
    table = 'biz_property'
