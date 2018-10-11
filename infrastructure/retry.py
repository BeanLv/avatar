# -*- coding: UTF-8 -*-

from functools import wraps


class RetryException:
    pass


class StopRetry:
    pass


class Retry:
    def __init__(self, times: int = 3, rest: int = 30):
        self.times = times
        self.rest = rest

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = None

            for i in range(0, self.times):
                try:
                    ret = func(*args, **kwargs)
                except StopRetry:
                    break
            else:
                raise Retry

            return ret

        return wrapper
