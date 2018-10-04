from enum import Enum


class OrderStatus(Enum):
    WAITING = 1
    WORKING = 2
    DONE = 3
    CANCELED = 4
    CLOSED = 5
