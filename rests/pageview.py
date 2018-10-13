# -*- coding: UTF-8 -*-

import datetime

from blueprints.rests import rests
from exceptions import RuntimeException

from dao.pageview import PageViewDAO
from models.model_binder import RequestParameterBinder


@rests.route('/pageview', methods=['POST'])
@RequestParameterBinder(name='source', required=False, value_type=int, from_json=True)
def create_pageview_record(source: int = None):
    try:
        record = {'date': datetime.datetime.utcnow().date().strftime('%Y-%m-%d'),
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
