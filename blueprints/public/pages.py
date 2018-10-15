# -*- coding: UTF-8 -*

import logging

from flask import Blueprint

import public

logger = logging.getLogger(__name__)

pages = Blueprint(name='publicpages',
                  import_name=public.__name__,
                  template_folder='templates',
                  url_prefix='/public/pages')

__import__('public.pages')
