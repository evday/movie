#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:08"

from app import app
from flask_script import Manager

manage = Manager(app)

if __name__ == "__main__":
    manage.run()