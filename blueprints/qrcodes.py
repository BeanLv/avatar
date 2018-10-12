# -*- coding: UTF-8 -*-

import logging

import flask
from flask import Blueprint

from config import config
from dao.qrcode import QrCodeDAO

logger = logging.getLogger(__name__)

qrcodes = Blueprint('qrcodes', __name__,
                    url_prefix='/qrcodes',
                    static_url_path='/static',
                    static_folder=config['minprogram']['qrcode']['storage'])


@qrcodes.route('/<int:qrcodeid>')
def qrcode_preview_page(qrcodeid):
    try:
        qrcode = QrCodeDAO.first_or_default(id=qrcodeid)

        if qrcode is None:
            return flask.render_template('404.html'), 404

        imagepath = '/qrcodes/static/{imagename}'.format(imagename=qrcode['imagename'])

        return flask.render_template('qrcodepreview.html',
                                     name=qrcode['name'],
                                     imagepath=imagepath)

    except Exception:
        logger.exception('二维码预览页面异常, qrcodeid: %s', qrcodeid)
        return flask.render_template('500.html'), 500
