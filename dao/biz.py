from dao.base_dao import BaseDAO


class BizDAO(BaseDAO):
    columns = ['id', 'name', 'operator', 'remark', 'disabled']
    table = 'biz'
