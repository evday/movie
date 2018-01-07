#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:09"
from flask import redirect,render_template
from . import home

@home.route("/")
def index():
    return "<h1 style='color:green'>this is home</h1>"

@home.route("/login")
def login():
    return render_template("home/login.html")

@home.route("/logout")
def logout():
    return redirect("home.login")

@home.route("/register")
def register():
    return render_template ("home/regist.html")

