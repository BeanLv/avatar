# -*- coding: UTF-8 -*-

import datetime
import ujson

from blueprints.rests import rests
from exceptions import RuntimeException

from dao.pageview import PageViewDAO
from dao.order_statistic_view import OrderStatisticView
from models.model_binder import RequestParameterBinder

from models.date_period import (TodayPeriod,
                                ThisWeekPeriod,
                                ThisMonthPeriod,
                                ThisSeasonPeriod,
                                HalfyearPeriod,
                                ThisYearPeriod)


@rests.route('/statistics/pageview')
@RequestParameterBinder(name='source', required=False, constructor=int)
def get_pageview_statistic(source: int = None):
    try:
        today = datetime.datetime.utcnow().date()
        periods = [TodayPeriod(today=today),
                   ThisWeekPeriod(today=today),
                   ThisMonthPeriod(today=today),
                   ThisSeasonPeriod(today=today),
                   HalfyearPeriod(today=today),
                   ThisYearPeriod(today=today)]

        statistic = {p.name: PageViewDAO.count(source=source,
                                               startdate=p.startdate.strftime('%Y-%m-%d'),
                                               enddate=p.enddate.strftime('%Y-%m-%d'))
                     for p in periods}

        return ujson.dumps(statistic)

    except Exception:
        raise RuntimeException('获取页面访问统计异常')


@rests.route('/statistics/order')
def get_order_statistic():
    try:
        return ujson.dumps(OrderStatisticView.get_statistic())
    except Exception:
        raise RuntimeException('获取订单统计异常')
