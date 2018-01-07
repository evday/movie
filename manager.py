#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:08"

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug = True)