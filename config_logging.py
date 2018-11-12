# -*- coding: UTF-8 -*-

import os
import logging
from logging.config import dictConfig

from utils.yaml_utils import load
from utils.dict_utils import deep_update_dict


def get_logging_config():
    files = ['resources/config.log.yml']
    if 'LOGCONFIG' in os.environ:
        files.append(os.environ.get('LOGCONFIG'))

    config = dict()
    for file in files:
        with open(file, encoding='UTF-8') as f:
            deep_update_dict(config, load(f))

    return files, config


def setup_logging_config():
    files, config = get_logging_config()

    dictConfig(config)

    logger = logging.getLogger(__name__)
    for f in files:
        logger.info('Load log config from %s', f)
