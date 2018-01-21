#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:09"
import uuid
import os
import datetime
import json

from flask import redirect,render_template,flash,session,request,url_for
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps

from . import home
from .forms import RegisterForm,LoginForm,UserDetailForm,PwdForm,CommentForm
from ..models import User,Userlog,Preview,Tag,Movie,Comment,Moviecol
from .. import db,app


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
@home.route("/user/",methods = ["GET","POST"])
def user():
    form = UserDetailForm()
    user = User.query.get(int(session["user_id"]))
    form.face.validators = []
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        file_face = secure_filename(form.face.data.filename)
        if not os.path.exists(app.config["FC_DIR"]):
            os.makedirs(app.config["FC_DIR"])
            os.chmod(app.config["FC_DIR"], "rw")
        user.face = change_filename(file_face)
        form.face.data.save(app.config["FC_DIR"] + user.face)

        name_count = User.query.filter_by(name=data["name"]).count()
        if data["name"] != user.name and name_count == 1:
            flash("昵称已经存在！", "err")
            return redirect(url_for("home.user"))

        email_count = User.query.filter_by(email=data["email"]).count()
        if data["email"] != user.email and email_count == 1:
            flash("邮箱已经存在！", "err")
            return redirect(url_for("home.user"))

        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if data["phone"] != user.phone and phone_count == 1:
            flash("手机号码已经存在！", "err")
            return redirect(url_for("home.user"))

        user.name = data["name"]
        user.email = data["email"]
        user.phone = data["phone"]
        user.info = data["info"]
        db.session.add(user)
        db.session.commit()
        flash("修改成功！", "ok")
        return redirect(url_for("home.user"))
    return render_template("home/user.html", form=form, user=user)

#修改会员密码
@home.route("/pwd",methods = ["GET","POST"])
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user= User.query.filter_by(name = session.get("name")).first()
        if not user.check_pwd(data.get("old_pwd")):
            flash("旧密码错误!","err")
            return redirect("home.pwd")
        user.pwd = generate_password_hash(data.get("new_pwd"))
        db.session.add(user)
        db.session.commit()
        flash("修改密码成功,请重新登录!","ok")
        return redirect(url_for("home.logout"))
    return render_template ("home/pwd.html",form = form)

#会员评论
@home.route("/comments/<int:page>/")
def comments(page = None):
    if not page:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(Comment.user_id == session["user_id"],Comment.movie_id == Movie.id).order_by(Comment.addtime.desc()).paginate(page = page,per_page = 10)
    return render_template ("home/comments.html",page_data = page_data)


#会员登录日志
@home.route("/loginlog/<int:page>/",methods = ["GET"])
def loginlog(page = None):
    if not page:
        page = 1
    page_data = Userlog.query.filter_by(user_id = int(session.get("user_id"))).order_by(Userlog.addtime.desc()).paginate(page=page,per_page = 10)
    return render_template ("home/loginlog.html",page_data = page_data)

#添加电影收藏
@home.route("/moviefav/add/",methods = ["GET"])
def moviefav():
    uid = request.args.get("uid","")
    mid = request.args.get("mid","")
    moviefav = Moviecol.query.filter_by(user_id = int(uid),movie_id = int(mid)).count()
    #等于1说明已经收藏过
    if moviefav == 1:
        data = dict(ok = 0)
    if moviefav == 0:
        moviefav = Moviecol(
            user_id = int(uid),
            movie_id = int(mid)
        )
        db.session.add(moviefav)
        db.session.commit()
        data = dict(ok = 1)
    return json.dumps(data)

@home.route("/moviefav/<int:page>/",methods = ["GET"])
def moviecol(page = None):
    if not page:
        page = 1
    page_data = Moviecol.query.join(User).join(Movie).filter(Moviecol.movie_id == Movie.id,Moviecol.user_id == session["user_id"]).order_by(Moviecol.addtime.desc()).paginate(page=page,per_page = 10)
    return render_template("home/moviecol.html",page_data = page_data)
#首页标签筛选
@home.route("/<int:page>/",methods = ["GET"])
@home.route("/")
def index(page = None):
    tags = Tag.query.all()
    page_data = Movie.query
    # 标签
    tid = request.args.get("tid",0)
    if int(tid) != 0:
        page_data = page_data.query.filter_by(tag_id = int(tid))
    #星级
    star = request.args.get("star",0)
    if int(star) != 0:
        page_data = page_data.query.filter_by(star = int(star))
    #时间
    time = request.args.get("time",0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.query.order_by(Movie.addtime.desc())
        else:
            page_data = page_data.query.order_by(Movie.addtime.asc())
    #播放量
    pm = request.args.get("pm",0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = page_data.query.order_by(Movie.playnum.desc())
        else:
            page_data = page_data.query.order_by(Movie.playnum.asc())
    #评论量
    cm = request.args.get("cm",0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = page_data.query.order_by(Movie.commentnum.desc())
        else:
            page_data = page_data.query.order_by(Movie.commentnum.asc())
    if not page:
        page = 1
    page_data = page_data.paginate(page = page,per_page = 8)
    p = dict(
        tid = tid,
        star = star,
        time = time,
        pm = pm,
        cm = cm
    )
    return render_template ("home/index.html",page_data = page_data,p = p,tags = tags)

#上映预告
@home.route("/animation")
def animation():
    data = Preview.query.all()
    return render_template ("home/animation.html",data = data)


#电影搜索
@home.route("/search/<int:page>/")
def search(page = None):
    if not page:
        page = 1
    key = request.args.get("key","")
    movie_count = Movie.query.filter(Movie.title.ilike("%"+key+"%")).count()
    page_data = Movie.query.filter(Movie.title.ilike("%"+key+"%")).order_by(Movie.addtime.desc()).paginate(page = page,per_page = 10)
    page_data.key = key
    return render_template ("home/search.html",page_data = page_data,key = key,movie_count = movie_count)

#电影播放
@home.route("/play/<int:id>/<int:page>/",methods = ["GET","POST"])
def play(id = None,page = None):
    movie = Movie.query.join(Tag).filter(Tag.id == Movie.tag_id,Movie.id == int(id)).first_or_404()
    moviecol = Moviecol.query.join(Movie).join(User).filter(Moviecol.user_id == session["user_id"],Moviecol.movie_id == movie.id).count()


    if not page:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(Comment.user_id == User.id,movie.id == Movie.id).order_by(Comment.addtime.desc()).paginate(page = page,per_page = 10)
    #播放次数加1
    movie.playnum = movie.playnum + 1
    form = CommentForm()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content = data.get("content"),
            movie_id = movie.id,
            user_id = session["user_id"]
        )
        db.session.add(comment)
        db.session.commit()
        #评论数加1
        movie.commentnum = movie.commentnum + 1
        db.session.add(movie)
        db.session.commit()
        flash("评论成功!","ok")
        return redirect(url_for("home.play",id = movie.id,page = 1))
    db.session.add(movie)
    db.session.commit()
    return render_template("home/play.html",movie = movie,page_data = page_data,form = form, moviecol = moviecol)