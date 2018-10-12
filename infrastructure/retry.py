# -*- coding: UTF-8 -*-

from functools import wraps
import time


class RetryFailed:
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
            for i in range(0, self.times):
                try:
                    func(*args, **kwargs)
                    time.sleep(self.rest)
                except StopRetry:
                    break
            else:
                raise RetryFailed

        return wrapper
