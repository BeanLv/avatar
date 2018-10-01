# -*- coding: UTF-8 -*-

from collections import Mapping


def deep_update_dict(d: dict, s: Mapping):
    """
    递归更新字典 d.
    如果 d[k] 和 s[k] 同时为 dict/Mapping，则不是直接赋值 d[k] = s[k],
    而是逐个将 m[k] 中的 k/v 更新到 d[k] 中，在将 m[k] 中的 k/v 更新到
    d[k] 中时，同样的也递归的做 dict/Mapping 类型的更新.
    """
    if d is None or not s:
        return

    for k, sv in s.items():
        dv = d.get(k)
        if isinstance(dv, dict) and isinstance(sv, Mapping):
            deep_update_dict(dv, sv)
        else:
            d[k] = sv
