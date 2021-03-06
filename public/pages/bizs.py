# -*- coding: UTF-8 -*-

import logging

import ujson
import flask

from config import config
from dao.biz import BizDAO
from dao.operator import OperatorDAO
from models.model_binder import QrCodeSourceBinder

from blueprints.public.pages import pages

logger = logging.getLogger(__name__)


@pages.route('/bizs/<int:bizid>')
@QrCodeSourceBinder()
def biz_preview(bizid, sourcename=None, sourcemobile=None):
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
        biz['boards'] = ujson.loads(biz['boards'])

        return flask.render_template('bizpreview.html',
                                     biz=biz,
                                     n=sourcename,
                                     m=sourcemobile,
                                     t=config['corp']['customerserver']['tel'])

    except:
        logger.exception('套餐预览页面异常 %d', bizid)
        return flask.render_template('500.html'), 500
