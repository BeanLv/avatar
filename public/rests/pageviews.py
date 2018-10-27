# -*- coding: UTF-8 -*-

import logging

from blueprints.public.rests import rests
from models.model_binder import RequestParameterBinder
from exceptions import RuntimeException
from dao.pageview import PageViewDAO
from utils import datetime_utils

logger = logging.getLogger(__name__)


@rests.route('/pageviews', methods=['POST'])
@RequestParameterBinder(name='source', required=False, value_type=int, from_json=True)
def create_pageview_record(source: int = 0):
    """
    没有二维码来源时 source 为 0。这样 MySQL 才会把同一天内 source 为 NULL 的记录索引为同一条。
    否则会有很多条 (2018-01-01, NULL) 的记录，因为 NULL 是不会相等的，所以不会是同一条记录。
    """
    try:
        record = {'date': datetime_utils.utc8now().date().strftime('%Y-%m-%d'),
                  'num': 1,
                  'source': source}

        if not source:
            record.pop('source')

        PageViewDAO.insert(record)

        return '', 201

    except Exception as e:
        raise RuntimeException('添加页面访问记录异常',
                               extra={'source': source}) \
            from e
