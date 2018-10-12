# -*- coding: UTF-8 -*-

import uuid

import ujson

from blueprints.rests import rests
from exceptions import RuntimeException, BusinessException
from dao import transaction
from dao.qrcode import QrCodeDAO

from models.model_binder import QrCodeModelBinder
from services import users as userservice
from services import qrcodes as qrcodeservice


@rests.route('/qrcodes')
def get_qrcodelist():
    try:
        qrcodelist = QrCodeDAO.all('id')

        return ujson.dumps(qrcodelist)

    except Exception as e:
        raise RuntimeException('获取二维码列表异常') from e


@rests.route('/qrcodes/<int:qrcodeid>')
def get_qrcode(qrcodeid):
    try:
        qrcode = QrCodeDAO.first_or_default(id=qrcodeid)

        if qrcode is None:
            return '二维码不存在', 404

        qrcode['owner'] = userservice.get_user_detail(qrcode['owner'])

        return ujson.dumps(qrcode)

    except Exception as e:
        raise RuntimeException('获取二维码详情异常',
                               extra={'qrcodeid': qrcodeid}) \
            from e


@rests.route('/qrcodes', methods=['POST'])
@QrCodeModelBinder()
def create_qrcode(name: str = None, owner: str = None, remark: str = None):
    try:
        with transaction():
            imagename = '{name}.jpg'.format(name=str(uuid.uuid1()).replace('-', ''))

            record = {'name': name, 'owner': owner, 'remark': remark, 'imagename': imagename}

            qrcodeid = QrCodeDAO.insert(record)

            qrcodeservice.generate_qrcode(qrcodeid=qrcodeid, imagename=imagename)

            return str(qrcodeid), 201

    except BusinessException as e:
        pass
    except Exception as e:
        raise RuntimeException('创建二维码异常',
                               extra={'name': name,
                                      'owner': owner,
                                      'remark': remark}) \
            from e


@rests.route('/qrcodes/<int:qrcodeid>', methods=['PATCH'])
@QrCodeModelBinder()
def update_qrcode(qrcodeid, name: str = None, owner: str = None, remark: str = None):
    try:
        record = {'name': name, 'owner': owner, 'remark': remark}
        QrCodeDAO.update(record, id=qrcodeid)
        return '', 204

    except Exception as e:
        raise RuntimeException('更新二维码异常',
                               extra={'name': name,
                                      'owner': owner,
                                      'remark': remark}) \
            from e