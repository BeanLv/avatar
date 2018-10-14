# -*- coding: UTF-8 -*-

import logging

import flask
from flask import Blueprint

from config import config
from dao.biz import BizDAO
from dao.bizproperty import BizPropertyDAO
from dao.operator import OperatorDAO

logger = logging.getLogger(__name__)

publicpage = Blueprint('publicpage', __name__,
                       static_folder=config['public']['staticfolder'],
                       static_url_path='/static',
                       url_prefix='/public')


@publicpage.route('/bizs/<int:bizid>')
def bizpreview(bizid):
    try:
        biz = BizDAO.first_or_default(id=bizid)

        if biz is None:
            return flask.render_template('404.html'), 404

        operator = OperatorDAO.first_or_default(id=biz['operator'])
        properties = BizPropertyDAO.all(biz=bizid)

        biz['operatorname'] = operator['name']
        biz['properties'] = {p['name']: p for p in properties}

        return flask.render_template('bizpreview.html', biz=biz)

    except:
        logger.exception('套餐预览页面异常 %d', bizid)
        return flask.render_template('500.html'), 500
