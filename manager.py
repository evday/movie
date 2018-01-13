#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:08"

from app import create_app
from flask.ext.script import Manager


app = create_app()
manage = Manager(app)


if __name__ == '__main__':
    manage.run()