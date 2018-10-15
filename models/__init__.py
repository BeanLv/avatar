from enum import Enum


class OrderStatus(Enum):
    WAITING = 1
    WORKING = 2
    DONE = 3
    CANCELED = 4
    CLOSED = 5


class OrderOperation(Enum):
    CREATE = 1
    DISPATCH = 2
    DEALWITH = 3
    FINISH = 4
    CANCEL = 5
    CLOSE = 6


class UserTag(Enum):
    ORDERNOTIFY = 1
