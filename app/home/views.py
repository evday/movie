#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:09"
import uuid
import os
import datetime

from flask import redirect,render_template,flash,session,request,url_for
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps

from . import home
from .forms import RegisterForm,LoginForm,UserDetailForm
from ..models import User,Userlog
from .. import db,create_app
app = create_app()

#登录装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "user" not in session:
            return redirect(url_for("home.login",next=request.url))
        return f(*args,**kwargs)
    return decorated_function

def change_filename(filename):
    file_info = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+uuid.uuid4().hex+file_info[-1]
    return filename



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

#修改会员资料
@home.route("/user",methods = ["GET","POST"])
@user_login_req
def user():
    form = UserDetailForm()
    user = User.query.get(int(session["user_id"]))
    form.face.validators = []
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.info.data = user.info
        form.phone.data = user.phone
    if form.validate_on_submit():
        data = form.data
        file_face = secure_filename(form.face.data.filename)
        if not os.path.exists (app.config ["FC_DIR"]):
            os.makedirs (app.config ["FC_DIR"])
            os.chmod (app.config ["FC_DIR"],"rw") # 读写的权限
        user_face = change_filename (file_face),
        form.face.data.save(app.config["FC_DIR"]+user_face)
        name_count = User.query.filter_by(name=data.get("name")).count()
        if user.name != data.get("user") and name_count == 1:
            flash("昵称已经存在!","err")
            return redirect(url_for("home.user"))
        email_count = User.query.filter_by (email = data.get ("email")).count ()
        if user.email != data.get("email") and email_count == 1:
            flash("邮箱已经存在!","err")
            return redirect(url_for("home.user"))
        phone_count = User.query.filter_by (phone = data.get ("phone")).count ()
        if user.phone != data.get("phone") and phone_count == 1:
            flash("手机号已经存在!","err")
            return redirect(url_for("home.user"))
        user.name = data.get("name")
        user.email = data.get("email")
        user.phone = data.get("phone")
        user.info = data.get("info")
        db.session.add(user)
        db.session.commit()
        flash("修改成功!","err")
        return redirect(url_for("home.user"))
    return render_template ("home/user.html",form=form,user=user)

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