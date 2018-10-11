# -*- coding: UTF-8 -*-

from dao.base_dao import BaseDAO


class QrCodeDAO(BaseDAO):
    table = 'qrcode'
    columns = ['id', 'name', 'remark', 'owner', 'disabled']
