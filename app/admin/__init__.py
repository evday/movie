#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:09"

from flask import Blueprint

admin = Blueprint("admin",__name__)

from . import views