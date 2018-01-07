#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:08"

from flask import Flask

def create_app():
    app = Flask(__name__)
    from app.admin import admin as admin_blueprint
    from app.home import home as home_blueprint
    app.register_blueprint(admin_blueprint,url_prefix="/admin")
    app.register_blueprint(home_blueprint)

    return app