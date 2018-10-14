# -*- coding: UTF-8 -*-

import logging

import flask
import ujson

from public import pages, rests
from dao.biz import BizDAO
from dao.operator import OperatorDAO
from dao.bizproperty import BizPropertyDAO

logger = logging.getLogger(__name__)


@pages.route('/bizs/<int:bizid>')
def biz_review(bizid):
    try:
        biz = BizDAO.first_or_default(id=bizid)

        if biz is None:
            return flask.render_template('404.html', message='套餐不存在'), 404

        operator = OperatorDAO.first_or_default(id=biz['operator'])
        properties = BizPropertyDAO.all(biz=bizid)

        biz['operatorname'] = operator['name']
        biz['properties'] = {p['name']: p for p in properties}

        return flask.render_template('bizpreview.html', biz=biz)

    except:
        logger.exception('套餐预览页面异常 %d', bizid)
        return flask.render_template('500.html'), 500


@rests.route('/bizs', methods=['GET'])
def bizs():
    try:
        operators = OperatorDAO.all('id', disabled=0)
        bizs = BizDAO.get_bizs_of_operators([o['id'] for o in operators])

        operatordict = {o['id']: o for o in operators}

        for o in operators:
            o['bizs'] = []
            o.pop('id')
            o.pop('disabled')

        for b in bizs:
            operatordict[b['operator']]['bizs'].append(b)
            b.pop('disabled')
            b.pop('operator')

        return ujson.dumps(operators)

    except Exception:
        logger.exception('获取套餐列表异常')
        return '接口错误', 500
