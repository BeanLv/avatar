# -*- coding: UTF-8 -*-

import os
import logging
from logging import config as loggingconfig

from utils.yaml_utils import load
from utils.dict_utils import deep_update_dict


def _load_config_from_files(*files):
    config = dict()
    for file in files:
        with open(file) as f:
            deep_update_dict(config, load(f))
    return config


def _setup_logging_config():
    files = ['resources/config.log.yml']
    if 'LOGCONFIG' in os.environ:
        files.append(os.environ.get('LOGCONFIG'))

    config = _load_config_from_files(*files)

    loggingconfig.dictConfig(config)

    logger = logging.getLogger(__name__)
    for f in files:
        logger.info('Load log config from "%s"', f)


def _load_config():
    files = ['resources/config.app.yml']
    if 'APPCONFIG' in os.environ:
        files.append(os.environ.get('APPCONFIG'))

    config = _load_config_from_files(*files)

    logger = logging.getLogger(__name__)
    for f in files:
        logger.info('Load app config from "%s"', f)

    return config


_setup_logging_config()

config = _load_config()
