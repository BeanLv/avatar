# -*- coding: UTF-8 -*-

import flask

from blueprints.public.pages import pages


@pages.route('/workbench')
def workbench():
    return flask.render_template('workbench.html')


@pages.route('/home')
def home():
    return flask.redirect('/public/pages/qrcodes/1')
