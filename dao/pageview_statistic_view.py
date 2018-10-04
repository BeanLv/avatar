import datetime

import dao
from models.date_period import (TodayPeriod,
                                ThisWeekPeriod,
                                ThisMonthPeriod,
                                ThisSeasonPeriod,
                                HalfyearPeriod,
                                ThisYearPeriod)


class PageviewStatisticView:
    sql_select = "SELECT SUM(`num`) " \
                 "FROM `pageview_statistic` " \
                 "WHERE `date` BETWEEN '{start_date}' AND '{end_date}'"

    @classmethod
    def get_statistic(cls, today=datetime.datetime.utcnow().date()) -> dict:
        periods = [TodayPeriod(today=today),
                   ThisWeekPeriod(today=today),
                   ThisMonthPeriod(today=today),
                   ThisSeasonPeriod(today=today),
                   HalfyearPeriod(today=today),
                   ThisYearPeriod(today=today)]

        sql = ' UNION ALL '.join([cls.sql_select.format(start_date=p.start_date.strftime('%Y-%m-%d'),
                                                        end_date=p.end_date.strftime('%Y-%m-%d'))
                                  for p in periods])

        connection = dao.connect()
        cursor = connection.cursor()
        cursor.execute(sql)

        nums = [o[0] for o in cursor.fetchall()]

        return dict(zip([p.name for p in periods],
                        [int(o) if o else 0 for o in nums]
                        )
                    )
