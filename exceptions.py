# -*- coding: UTF-8 -*-

class AvatarException(Exception):
    """avatar 系统所有异常的基类"""

    def __init__(self, msg: str, extra: dict = None):
        """
        :param msg: 描述信息
        :param extra: 附加信息，在打印异常的时候按照 key:value 逐行输出
        """
        self.msg = msg
        self.extra = extra
        super().__init__(msg)


class RuntimeException(AvatarException):
    """
    代码运行时异常，这是内部为非预期异常，通常返回 500 给调用方
    """

    def __str__(self):
        extramsg = '\n'.join(['{}: {}'.format(k, v) for k, v in self.extra.items()]) if self.extra else None
        return '{}\n{}'.format(self.msg, extramsg) if extramsg else self.msg


class BusinessException(AvatarException):
    """
    业务异常，当操作不满足一定条件时返回这个异常，包括状态码和详细信息
    """

    def __init__(self, errcode: int, msg: str, extra: dict = None):
        """
        :param errcode: 错误状态码
        :param msg: 描述信息
        :param extra: 附加信息，在打印异常的时候按照 key:value 逐行输出
        """
        self.errcode = errcode
        self.msg = msg
        self.extra = extra
        super().__init__(msg)

    def __str__(self):
        extramsg = '\n'.join(['{}: {}'.format(k, v) for k, v in self.extra.items()]) if self.extra else None
        return '{}\nerrcode: {}\n{}'.format(self.msg, self.errcode, extramsg) if extramsg else \
            '{}\nerrcode: {}'.format(self.msg, self.errcode)
