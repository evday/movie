#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:09"
import uuid

from flask import redirect,render_template,flash,session,request,url_for
from werkzeug.security import generate_password_hash
from functools import wraps

from . import home
from .forms import RegisterForm,LoginForm
from ..models import User,Userlog
from .. import db

#登录装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args,**kwargs)
        if "user" not in session:
            return redirect(url_for("home.login",next=request.url))
        return f(*args,**kwargs)
    return decorated_function





#会员登录
@home.route("/login",methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name = data.get("name")).first()
        if not user.check_pwd(data.get("pwd")):
            flash("密码错误!",'err')
        session["user"] = user.name
        session["user_id"] = user.id
        userlog = Userlog(user_id = user.id,ip = request.remote_addr)
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template("home/login.html",form =form)

#注销
@home.route("/logout",methods = ["GET"])
@user_login_req
def logout():
    session.pop("user")
    session.pop("user_id")
    return redirect(url_for("home.login"))


#会员注册
@home.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user  = User(
            name = data.get("name"),email = data.get("email"),
            phone = data.get("phone"),pwd = generate_password_hash(data.get("pwd")),
            uuid = uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功!","ok")
    return render_template ("home/regist.html",form = form)

@home.route("/user")
@user_login_req
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

@home.route("/moviefav")
def moviefav():
    return render_template ("home/moviefav.html")

@home.route("/")
def index():
    return render_template ("home/index.html")

@home.route("/animation")
def animation():
    return render_template ("home/animation.html")

@home.route("/search")
def search():
    return render_template ("home/search.html")