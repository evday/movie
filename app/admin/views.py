#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:09"
from flask import render_template,redirect,url_for
from . import admin

@admin.route("/")
def index():
    return render_template("admin/index.html")

@admin.route("/login")
def login():
    return render_template("admin/login,html")

@admin.route("/logout")
def login():
    return redirect(url_for("admin.login"))


@admin.route("/pwd")
def pwd():
    return render_template("admin/pwd,html")

@admin.route("/tag/add/")
def tag_add():
    return render_template("admin/tag_add,html")

@admin.route("/tag/list/")
def tag_list():
    return render_template("admin/tag_list,html")

@admin.route("/movie/add/")
def movie_add():
    return render_template("admin/movie_add,html")

@admin.route("/movie/list")
def movie_list():
    return render_template("admin/movie_add,html")

@admin.route("/preview/add/")
def preview_add():
    return render_template("admin/preview_add,html")

@admin.route("/preview/list/")
def preview_list():
    return render_template("admin/preview_add,html")

@admin.route("/user/list/")
def user_list():
    return render_template("admin/user_list,html")

@admin.route("/user/view/")
def user_view():
    return render_template("admin/user_view,html")

@admin.route("/comment/list/")
def comment_list():
    return render_template("admin/comment_list,html")

@admin.route("/moviefav/list/")
def moviefav_list():
    return render_template("admin/moviefav_list,html")

@admin.route("/oplog/list/")
def oplog_list():
    return render_template("admin/oplog_list,html")

@admin.route("/adminloginlog/list/")
def adminloginlog_list():
    return render_template("admin/adminloginlog_list,html")

@admin.route("/userloginlog/list/")
def userloginlog_list():
    return render_template("admin/userloginlog_list,html")

@admin.route("/role/add/")
def role_add():
    return render_template("admin/role_add,html")

@admin.route("/role/list/")
def role_list():
    return render_template("admin/role_list,html")

@admin.route("/auth/add/")
def auth_add():
    return render_template("admin/auth_add,html")

@admin.route("/auth/list/")
def auth_list():
    return render_template("admin/auth_list,html")