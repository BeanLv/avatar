# -*- coding: UTF-8 -*-

from unittest.mock import patch

from utils.yaml_utils import load


@patch.dict('os.environ', {'NAME': 'avatar'})
def test_yamlloader():
    d = load(
        """
        name: !!os/env NAME
        age: 1
        married: false 
        """)
    assert d == {'name': 'avatar',
                 'age': 1,
                 'married': False}