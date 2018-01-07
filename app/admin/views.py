#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:09"
from . import admin

@admin.route("/")
def index():
    return "<h1 style='color:red'>this is admin</h1>"