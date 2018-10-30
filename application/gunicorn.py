# -*- coding: UTF-8 -*-

import os
import multiprocessing

bind = '0.0.0.0:5000'

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'

errorlog = os.path.expandvars('${HOME}/avatar/logs/server')

keyfile = os.path.expandvars('${HOME}/avatar/ssh/private.key')
certfile = os.path.expandvars('${HOME}/avatar/ssh/public.pem')
