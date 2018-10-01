# -*- coding: UTF-8 -*-

import pytest

from utils.dict_utils import deep_update_dict


@pytest.fixture(name='d', autouse=True)
def d():
    return {'a': 1,
            'b': {'c': 2},
            'd': {'e': 3,
                  'f': {'g': 4,
                        'h': 5
                        }
                  }
            }


@pytest.mark.parametrize('s, expect', [
    (None, d()),
    ({'a': None, 'b': 2, 'c': 3}, {'a': None, 'b': 2, 'c': 3, 'd': {'e': 3, 'f': {'g': 4, 'h': 5}}}),
    ({'d': {'f': {'g': {'h': 2}}}}, {'a': 1, 'b': {'c': 2}, 'd': {'e': 3, 'f': {'g': {'h': 2}, 'h': 5}}})
])
def test_deep_update_dict(d, s, expect):
    deep_update_dict(d, s)
    assert d == expect
