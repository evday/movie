#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,22:28"

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/movie?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


    @staticmethod
    def init_app(app):
        pass