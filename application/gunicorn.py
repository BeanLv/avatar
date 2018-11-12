# -*- coding: UTF-8 -*-

import os
import sys
import multiprocessing


def redirect_print():
    sys.stdout = open(os.devnull, 'w')


def get_logging_config():
    from config_logging import get_logging_config
    _, config = get_logging_config()
    return config


bind = '0.0.0.0:5000'

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'

logconfig_dict = get_logging_config()

keyfile = os.path.expandvars('${HOME}/avatar/ssh/private.key')
certfile = os.path.expandvars('${HOME}/avatar/ssh/public.pem')

redirect_print()
