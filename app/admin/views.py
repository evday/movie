#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:09"
from flask import render_template,redirect,url_for
from . import admin

@admin.route("/")
def index():
    return "<h1 style='color:red'>this is admin</h1>"

@admin.route("/login")
def login():
    return render_template("admin/login,html")

@admin.route("/logout")
def login():
    return redirect(url_for("admin.login"))