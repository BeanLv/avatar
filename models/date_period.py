# -*- coding: UTF-8 -*-

import datetime
from datetime import date


class DatePeriod:
    def __init__(self, start_date: date, end_date: date):
        self._start_date = start_date
        self._end_date = end_date

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def name(self):
        return self.__class__.__name__.lower().replace('period', '')


class TodayPeriod(DatePeriod):
    def __init__(self, today: date):
        super().__init__(start_date=today, end_date=today)

    def __hash__(self):
        return 0


class ThisWeekPeriod(DatePeriod):
    def __init__(self, today: date):
        super().__init__(start_date=date(year=today.year, month=today.month, day=today.day) \
                                    - datetime.timedelta(days=today.weekday()),
                         end_date=today)

    def __hash__(self):
        return 1


class ThisMonthPeriod(DatePeriod):
    def __init__(self, today: date):
        super().__init__(start_date=date(year=today.year, month=today.month, day=1),
                         end_date=today)

    def __hash__(self):
        return 2


class ThisSeasonPeriod(DatePeriod):
    def __init__(self, today: date):
        super().__init__(start_date=date(today.year, month=1 + 3 * ((today.month + 2) // 3 - 1), day=1),
                         end_date=today)

    def __hash__(self):
        return 3


class HalfyearPeriod(DatePeriod):
    def __init__(self, today: date):
        super().__init__(
            start_date=date(year=today.year, month=1 if today.month < 7 else 7, day=1),
            end_date=today)

    def __hash__(self):
        return 4


class ThisYearPeriod(DatePeriod):
    def __init__(self, today: date):
        super().__init__(start_date=date(year=today.year, month=1, day=1),
                         end_date=today)

    def __hash__(self):
        return 5
