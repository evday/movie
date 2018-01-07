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

@home.route("/user")
def user():
    return render_template ("home/user.html")

@home.route("/pwd")
def pwd():
    return render_template ("home/pwd.html")

@home.route("/comments")
def comments():
    return render_template ("home/comments.html")

@home.route("/loginlog")
def loginlog():
    return render_template ("home/loginlog.html")