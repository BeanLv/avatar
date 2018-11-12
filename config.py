# -*- coding: UTF-8 -*-

import os
import logging

from utils.yaml_utils import load
from utils.dict_utils import deep_update_dict
from config_logging import setup_logging_config


def _load_config_from_files(*files):
    config = dict()
    for file in files:
        with open(file, encoding='UTF-8') as f:
            deep_update_dict(config, load(f))
    return config


def _load_config():
    files = ['resources/config.app.yml']
    if 'APPCONFIG' in os.environ:
        files.append(os.environ.get('APPCONFIG'))

    config = _load_config_from_files(*files)

    logger = logging.getLogger(__name__)
    for f in files:
        logger.info('Load app config from "%s"', f)

    return config


setup_logging_config()

config = _load_config()
