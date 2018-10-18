# -*- coding: UTF-8 -*-

import logging

import flask

from config import config
from dao.biz import BizDAO
from dao.operator import OperatorDAO
from dao.qrcode import QrCodeDAO
from services import users as userservice

from blueprints.public.pages import pages

logger = logging.getLogger(__name__)


@pages.route('/bizs/<int:bizid>')
def biz_preview(bizid):
    try:
        biz = BizDAO.first_or_default(id=bizid)

        if biz is None:
            logger.warning('用户访问一个不存在的套餐. bizid=%d', bizid)
            return flask.render_template('404.html', message='套餐不存在'), 404

        operator = OperatorDAO.first_or_default(id=biz['operator'])
        if operator is None:
            logger.warning('用户访问一个供应商不存在的套餐, bizid=%d', bizid)
            return flask.render_template('404.html', message='套餐不存在'), 404

        biz['operatorname'] = operator['name']

        user, sourcename, sourcemobile = None, None, None

        source = flask.request.args.get('source')
        if source and source.isdigit():
            qrcode = QrCodeDAO.first_or_default(id=int(source))
            if qrcode and qrcode.get('owner'):
                user = userservice.get_user_detail(qrcode.get('owner'))

        if user:
            sourcename = user['name']
            sourcemobile = user['mobile']

        if not sourcename or not sourcemobile:
            sourcename = config['corp']['manager']['name']
            sourcemobile = config['corp']['manager']['mobile']

        return flask.render_template('bizpreview.html',
                                     biz=biz,
                                     n=sourcename[0],
                                     m=sourcemobile)

    except:
        logger.exception('套餐预览页面异常 %d', bizid)
        return flask.render_template('500.html'), 500
