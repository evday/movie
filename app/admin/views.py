#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:09"
import os
import uuid
import datetime
from functools import wraps
from flask import render_template,redirect,url_for,session,request
from flask import flash
from werkzeug.utils import secure_filename
from . import admin
from .. import db,create_app
from .forms import LoginForm,TagForm,MovieForm,PreviewForm,PwdForm
from ..models import Admin,Adminlog,Tag,Movie,Preview,User,Comment,Moviecol
app = create_app()


#登陆装饰器
def admin_login_req(f):
    @wraps(f)
    def decorate_function(*args,**kwargs):
        if not session.get("user_info"):
            return redirect(url_for("admin.login",next = request.url))
        return f(*args,**kwargs)
    return decorate_function

#修改文件名
def change_filename(filename):
    file_info = os.path.splitext(filename) # 根据后缀分割
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+ str(uuid.uuid4().hex)+file_info[-1]
    return filename

#首页
@admin.route("/")
@admin_login_req
def index():

    return render_template("admin/index.html")
#登陆
@admin.route("/login",methods = ["GET","POST"])
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

#注销
@admin.route("/logout")
@admin_login_req
def logout():
    session.pop("admin")
    session.pop("admin_id")
    return redirect(url_for("admin.login"))


@admin.route("/pwd")
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name = session.get("name")).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data.get("new_pwd"))
        db.session.add(admin)
        db.session.commit()
        flash("修改密码成功!,请重新登陆!","ok")
        return redirect(url_for("admin.logout"))
    return render_template("admin/pwd,html",form = form)


# 标签列表
@admin.route("/tag/list/<int:page>/",methods = ["GET"])
@admin_login_req
def tag_list(page = None):
    if not page:
        page = 1
    page_data = Tag.query.order_by(Tag.addtime.desc()).paginate(page=1,per_page = 1)

    return render_template("admin/tag_list,html",page_data=page_data)
# 增加标签
@admin.route("/tag/add/",methods = ["GET","POST"])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name = data.get("name")).count()
        if tag:
            flash("标签已存在",category = "err")
            return redirect(url_for("admin.tag_add"))
        tag = Tag(
            name = data.get("name")
        )
        db.session.add(tag)
        db.session.commit()
        flash("添加成功",category = "ok")
        return redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add,html")

#删除标签
@admin.route("/tag/del/<int:id>/",methods = ["GET"])
@admin_login_req
def tag_delete(id = None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.add(tag)
    db.session.commit()
    flash("删除标签成功！",category = "ok")
    return redirect(url_for("admin.tag_list",page=1))

#编辑标签
@admin.route("/tag/edit/<int:id>/",methods = ["GET","POST"])
@admin_login_req
def tag_edit(id):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name = data.get("name")).count()
        if tag:
            flash("标签名称已存在!",category = "err")
            return redirect(url_for("admin.tag_edit",id=id))
        tag.name = data.get("name")
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功!",category = "ok")
        return redirect(url_for("admin.tag_edit",id=id))
    return render_template("admin/tag_edit,html",tag=tag,form=form)

#添加电影
@admin.route("/movie/add/")
@admin_login_req
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)#保证文件安全
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"],"rw") # 读写的权限
        url = change_filename(file_url),
        logo = change_filename(file_logo)
        form.url.data.save(app.config["UP_DIR"]+url)
        form.logo.data.save(app.config["UP_DIR"]+logo)
        movie = Movie(
            title = data.get("title"),
            url = url,
            info = data.get("info"),
            logo = logo,
            star = int(data.get("star")),
            playnum = 0,
            commentnum = 0,
            tag_id = int(data.get("tag_id")),
            area = data.get("area"),
            release_time = data.get("release_time"),
            length = data.get("length")
        )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影成功!","ok")
        return redirect(url_for("admin.movie_add"))
    return render_template("admin/movie_add,html",form=form)
#电影列表
@admin.route("/movie/list/<int:page>/",methods = ["GET"])
@admin_login_req
def movie_list(page):
    if page is None:
        page = 1
    page_data = Movie.qury.join(Tag).filter(Tag.id == Movie.tag_id).order_by(Movie.addtime.desc()).paginate(page = page,per_page = 10)
    return render_template("admin/movie_add,html",page_data=page_data)
# 删除电影
@admin.route("/movie/del/<int:id>/",methods = ["GET"])
@admin_login_req
def movie_del(id = None):
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash("删除电影成功!","ok")
    return redirect(url_for("admin.movie_list",page=1))

#修改电影
@admin.route("/movie/edit/<int:id>/",methods = ["GET","POST"])
@admin_login_req
def movie_edit(id=None):
    form = MovieForm()
    movie = Movie.query.get_or_404(int(id))
    if request.method == "GET":
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title = data.get("title")).count()
        if movie_count == 1 and movie.title != data.get("title"):
            flash("片名已存在!","err")
            return redirect(url_for("admin.movie_edit",id=id))

        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"],"rw")

        if form.url.data.filename != "":
            file_url =secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config["UP_DIR"]+ movie.url)

        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"]+ movie.logo)
        movie.star = data.get("star"),
        movie.tag_id = data.get("tag_id"),
        movie.info = data.get("info"),
        movie.title = data.get("title"),
        movie.area = data.get("area"),
        movie.length = data.get("length"),
        movie.release_time = data.get("release_time"),
        db.session.add(movie)
        db.session.commit()
        flash("修改电影成功!","ok")
        return redirect(url_for("admin.movie_edit",id=movie.id))
    return render_template("admin/movie_edit.html",form=form,movie=movie)

#添加电影预告
@admin.route("/preview/add/",methods = ["GET","POST"])
@admin_login_req
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"],"rw")
            logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"]+logo)
            preview= Preview(
                title = data.get("title"),
                logo = logo
            )
            db.session.add(preview)
            db.session.commit()
            flash("添加预告成功!")
            return redirect(url_for("admin.preview_add"))
    return render_template("admin/preview_add,html",form = form)
#电影预告列表
@admin.route("/preview/list/<int:page>",methods = ["GET"])
@admin_login_req
def preview_list(page = None):
    if not page:page = 1
    page_data = Preview.query.order_by(Preview.addtime.desc()).paginate(page = page,per_page = 10)
    return render_template("admin/preview_add,html",page_data = page_data)
#电影预告删除
@admin.route("/preview/del/<int:id>/",methods = ["GET"])
@admin_login_req
def preview_del(id=None):
    preview = Preview.query.get_or_404(int(id))
    db.session.add(preview)
    db.session.commit()
    flash("删除电影预告成功!",'ok')
    return redirect(url_for("admin.preview_list",page=1))
#修改电影预告
@admin.route("/preview/edit/<int:id>/",methods = ["GET"])
@admin_login_req
def preview_edit(id):
    form = PreviewForm()
    form.logo.validators = [] #编辑的时候数据里是有值的，这里不需要做判断
    preview = Preview.query.get_or_404(int(id))
    if request.method == "GET":
        form.title.data = preview.title
    if form.validate_on_submit():
        data = form.data
        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"]+preview.log)
        preview.title = data.get("title")
        db.session.add(preview)
        db.session.commit()
        flash("修改预告成功!",'ok')
        return redirect(url_for("admin.preview_edit",id=id))
    return render_template("admin/preview_eidt.html",form=form,preview=preview)

#会员列表
@admin.route("/user/list/<int:page>/",methods = ["GET"])
@admin_login_req
def user_list(page = None):
    if not page:
        page = 1
    page_data = User.query.order_by(User.addtime.desc()).paginate(page=page,per_page = 10)
    return render_template("admin/user_list,html",page_data = page_data)

#查看会员
@admin.route("/user/view/<int:id>/",methods = ["GET"])
@admin_login_req
def user_view(id= None):
    user = User.query.get_or_404(id = int(id))
    return render_template("admin/user_view,html",user=user)

#删除会员
@admin.route("/user/del/<int:id>/",methods =["GET"])
@admin_login_req
def user_del(id = None):
    user = User.query.get_or_404(id = int(id))
    db.session.add(user)
    db.session.commit()
    flash("删除会员成功!","ok")
    return redirect(url_for("admin.user_list",page=1))

#评论列表
@admin.route("/comment/list/<int:page>/")
@admin_login_req
def comment_list(page = None):
    if not page:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(Comment.movie_id == Movie.id,Comment.user_id == User.id).order_by(Comment.addtime.desc()).paginate(page=page,per_page = 10)
    return render_template("admin/comment_list,html",page_data = page_data)

#删除评论
@admin.route("/comment/del/<int:id>/",methods = ["GET"])
@admin_login_req
def comment_del(id=None):
    comment = Comment.query.get_or_404(id=int(id))
    db.session.add(comment)
    db.session.commit()
    flash("删除评论成功!",'ok')
    return redirect(url_for("admin.comment_list",page=1))

#电影收藏列表
@admin.route("/moviefav/list/<int:page>/",methods = ["GET"])
def moviefav_list(page=None):
    if not page:
        page =1
    page_data = Moviecol.query.join(Movie).join(User).filter(Moviecol.movie_id == Movie.id,Moviecol.user_id == User.id).order_by(Moviecol.addtime.desc()).paginate(page=page,per_page = 10)
    return render_template("admin/moviefav_list,html",page_data = page_data)

#电影收藏删除
@admin.route("/moviefav/del/<int:id>/",methods = ["GET"])
def moviefav_del(id = None):
    moviefav = Moviecol.query.get_or_404(id = int(id))
    db.session.add(moviefav)
    db.session.commit()
    flash("删除收藏成功!","ok")
    return redirect(url_for("admin.moviefav_list",page =1 ))
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