#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:09"
from functools import wraps
from flask import render_template,redirect,url_for,session,request
from flask import flash
from . import admin
from .. import db
from .forms import LoginForm
from ..models import Admin,Adminlog


def admin_login_req(f):
    @wraps(f)
    def decorate_function(*args,**kwargs):
        if not session.get("user_info"):
            return redirect(url_for("admin.login",next = request.url))
        return f(*args,**kwargs)
    return decorate_function


@admin.route("/")
@admin_login_req
def index():

    return render_template("admin/index.html")

@admin.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name = data.get("account")).first()
        if not admin.check_pwd(data.get("pwd")):
            flash("密码错误!",category = "err")
            return redirect(url_for("admin.login"))
        session["admin"] = data.get("account")
        session["admin_id"] = admin.id
        adminlog = Adminlog(
            admin_id = admin.id,
            ip = request.remote_addr, #获取Ip
        )
        db.session.add(adminlog)
        db.session.commit()
    return render_template("admin/login,html",form=form)

@admin.route("/logout")
@admin_login_req
def logout():
    session.pop("admin")
    session.pop("admin_id")
    return redirect(url_for("admin.login"))


@admin.route("/pwd")
@admin_login_req
def pwd():
    return render_template("admin/pwd,html")

@admin.route("/tag/add/")
@admin_login_req
def tag_add():
    return render_template("admin/tag_add,html")

@admin.route("/tag/list/")
@admin_login_req
def tag_list():
    return render_template("admin/tag_list,html")

@admin.route("/movie/add/")
@admin_login_req
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

@admin.route("/admin/add/")
def admin_add():
    return render_template("admin/admin_add,html")

@admin.route("/admin/list/")
def admin_list():
    return render_template("admin/admin_list,html")