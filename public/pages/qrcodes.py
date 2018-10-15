# -*- coding: UTF-8 -*-

import logging

import flask

from dao.qrcode import QrCodeDAO
from services import qrcodes as qrcodeservice

from blueprints.public.pages import pages

logger = logging.getLogger(__name__)


@pages.route('/qrcodes/<int:qrcodeid>')
def qrcode_preview(qrcodeid):
    try:
        qrcode = QrCodeDAO.first_or_default(id=qrcodeid)

        if qrcode is None:
            return flask.render_template('404.html', message='二维码不存在'), 404

        return flask.render_template('qrcodepreview.html',
                                     name=qrcode['name'],
                                     imagepath=qrcodeservice.get_qrcode_url_path(qrcode['imagename']))

    except Exception:
        logger.exception('二维码预览页面异常, qrcodeid: %s', qrcodeid)
        return flask.render_template('500.html'), 500
