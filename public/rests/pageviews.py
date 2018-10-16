# -*- coding: UTF-8 -*-

import logging
import datetime

from blueprints.public.rests import rests
from models.model_binder import RequestParameterBinder
from exceptions import RuntimeException
from dao.pageview import PageViewDAO

logger = logging.getLogger(__name__)


@rests.route('/pageviews', methods=['POST'])
@RequestParameterBinder(name='source', required=False, value_type=int, from_json=True)
def create_pageview_record(source: int = None):
    try:
        record = {'date': datetime.datetime.utcnow().date().strftime('%Y-%m-%d'),
                  'num': 1,
                  'source': source}

        logger.debug('新增页面统计: %s', record)

        if not source:
            record.pop('source')

        PageViewDAO.insert(record)

        return '', 201

    except Exception as e:
        raise RuntimeException('添加页面访问记录异常',
                               extra={'source': source}) \
            from e
