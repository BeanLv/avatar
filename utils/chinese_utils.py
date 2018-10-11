# -*- coding: UTF-8 -*-

from pypinyin import lazy_pinyin, load_phrases_dict

load_phrases_dict({'覃': [['Qin']]})


def get_pinying(string: str):
    return ''.join([w.title() for w in lazy_pinyin(string)])
