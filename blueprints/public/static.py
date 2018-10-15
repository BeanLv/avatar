# -*- coding: UTF-8 -*

from flask import Blueprint

from config import config

import public

static = Blueprint(name='public',
                   import_name=public.__name__,
                   static_folder=config['public']['staticfolder'],
                   static_url_path='/static',
                   url_prefix='/public')
