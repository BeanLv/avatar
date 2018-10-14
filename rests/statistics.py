# -*- coding: UTF-8 -*-

import datetime
import ujson

from blueprints.rests import rests
from exceptions import RuntimeException

from dao.order import OrderDAO
from dao.pageview import PageViewDAO
from models.model_binder import RequestParameterBinder

from models import OrderStatus
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

        statistic = {p.name: PageViewDAO.sum(source=source,
                                             startdate=p.startdate.strftime('%Y-%m-%d'),
                                             enddate=p.enddate.strftime('%Y-%m-%d'))
                     for p in periods}

        return ujson.dumps(statistic)

    except Exception as e:
        raise RuntimeException('获取页面访问统计异常',
                               extra={'source': source}) \
            from e


@rests.route('/statistics/order')
@RequestParameterBinder(name='handler', required=False)
@RequestParameterBinder(name='source', required=False, constructor=int)
def get_order_statistic(handler: str = None, source: int = None):
    try:
        today = datetime.datetime.utcnow().date()
        periods = [TodayPeriod(today=today),
                   ThisWeekPeriod(today=today),
                   ThisMonthPeriod(today=today),
                   ThisSeasonPeriod(today=today),
                   HalfyearPeriod(today=today),
                   ThisYearPeriod(today=today)]

        statistic = {p.name: OrderDAO.count(handler=handler,
                                            source=source,
                                            startdate=p.startdate.strftime('%Y-%m-%d'),
                                            enddate=p.enddate.strftime('%Y-%m-%d'))
                     for p in periods}

        for status in [OrderStatus.WAITING, OrderStatus.WORKING, OrderStatus.DONE]:
            statistic[status.name.lower()] = OrderDAO.count(handler=handler,
                                                            source=source,
                                                            status=status.value)

        return ujson.dumps(statistic)

    except Exception as e:
        raise RuntimeException('获取订单统计异常',
                               extra={'handler': handler,
                                      'source': source}) \
            from e
