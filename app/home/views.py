#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:09"

from . import home

@home.route("/")
def index():
    return "<h1 style='color:green'>this is home</h1>"