from dao.base_dao import BaseDAO


class OrderDAO(BaseDAO):
    columns = ['id', 'status', 'biz', 'openid', 'realname', 'nickname', 'headimgurl', 'mobile',
               'address', 'lon', 'lat', 'installtime']
    table = "`order`"
