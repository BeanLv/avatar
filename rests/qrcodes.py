# -*- coding: UTF-8 -*-

import logging

import ujson

from blueprints.rests import rests
from exceptions import RuntimeException, BusinessException
from dao import transaction
from dao.qrcode import QrCodeDAO
from models.model_binder import QrCodeModelBinder
from services import users as userservice
from services import qrcodes as qrcodeservice

logger = logging.getLogger(__name__)


@rests.route('/qrcodes')
def get_qrcodelist():
    try:
        qrcodelist = QrCodeDAO.all('id')

        for qrcode in qrcodelist:
            owner = userservice.get_user_detail(qrcode['owner'])
            if not owner:
                qrcode['owner'] = None
                qrcode['ownername'] = None
            else:
                qrcode['ownername'] = owner['name']

        return ujson.dumps(qrcodelist)

    except Exception as e:
        raise RuntimeException('获取二维码列表异常') from e


@rests.route('/qrcodes', methods=['POST'])
@QrCodeModelBinder()
def create_qrcode(name: str = None, owner: str = None, remark: str = None):
    try:
        with transaction():
            record = {'name': name, 'owner': owner, 'remark': remark, 'imagename': ''}
            qrcodeid = QrCodeDAO.insert(record)
            qrcodeservice.generate_qrcode(qrcodeid=qrcodeid, imagename='%d.jpg' % qrcodeid)
            QrCodeDAO.update({'imagename': '%d.jpg' % qrcodeid}, id=qrcodeid)

            return str(qrcodeid), 201

    except BusinessException as e:
        logger.exception('创建二维码业务错误')
        return e.msg, e.errcode

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
