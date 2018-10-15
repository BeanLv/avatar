# -*- coding: UTF-8 -*

import logging

import flask
from flask import Blueprint

import public

logger = logging.getLogger(__name__)

pages = Blueprint(name='publicpages',
                  import_name=public.__name__,
                  template_folder='templates',
                  url_prefix='/public/pages')


# 默认的 page 路由
@pages.route('<page>')
def render_page(page):
    return flask.render_template('%s.html' % page)


__import__('public.pages')
