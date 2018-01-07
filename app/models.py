#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:14"
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.config ["SQLALCHEMY_DATABASE_URL"] = "mysql://root:@localhost:3306/movie?charset=utf8"
app.config ["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy (app)


class User (db.Model):
    '''
    用户模型
    '''
    __tablename__ = "user"
    id = db.Column (db.Integer,primary_key = True,autoincrement = True)
    name = db.Column (db.String (20),unique = True)
    pwd = db.Column (db.String (20))
    email = db.Column (db.String (64),unique = True)
    phone = db.Column (db.String (64),unique = True)
    info = db.Column (db.Text)
    face = db.Column (db.String (255))
    add_time = db.Column (db.DateTime,index = True,default = datetime.datetime.utcnow ())
    uuid = db.Column (db.String (255),unique = True)#唯一标识符
    userlog = db.Column (db.relationship ("Userlog",backref = "user"))#会员日志外键关联关系
    comments = db.Column (db.relationship ("Comment",backref = "user"))#评论外键关联关系
    moviefavs = db.Column (db.relationship ("Moviefav",backref = "user"))#收藏外键关联关系

    def __repr__ (self):
        return "<User %r>" % self.name


class Userlog (db.Model):
    '''
    会员登陆日志模型
    '''
    __tablename__ = "userlog"
    db.Column (db.Integer,primary_key = True,autoincrement = True)
    user_id = db.Column (db.Integer,db.ForeignKey ("user.id"))
    ip = db.Column (db.String (64))
    add_time = db.Column (db.DateTime,index = True,default = datetime.datetime.utcnow ())

    def __repr__ (self):
        return "<Userlog %r>" % self.id


class Tag (db.Model):
    '''
    电影标签模型
    '''
    __tablename__ = "tag"
    id = db.Column (db.Integer,primary_key = True,autoincrement = True)
    name = db.Column (db.String (64),unique = True)
    add_time = db.Column (db.DateTime,index = True,default = datetime.datetime.utcnow ())
    movies = db.Column (db.relationship ("Movie",backref = "tag")) #电影外键关联关系

    def __repr__ (self):
        return "<Tag %r>" % self.name


class Movie (db.Model):
    '''
    电影模型
    '''
    __tablename__ = "movie"
    id = db.Column (db.Integer,primary_key = True,autoincrement = True)
    title = db.Column (db.String (255),unique = True)
    url = db.Column (db.String (255),unique = True)
    info = db.Column (db.Text) #电影介绍
    logo = db.Column (db.String (255),unique = True)
    star = db.Column (db.SmallInteger) #推荐指数
    play_num = db.Column (db.BigInteger) #播放数
    comment_num = db.Column (db.BigInteger)
    area = db.Column (db.String (255)) #上映地区
    release_time = db.Column (db.Date) #上映时间
    length = db.Column (db.String (64))
    add_time = db.Column (db.DateTime,index = True,default = datetime.datetime.utcnow ())
    tag_id = db.Column (db.Integer,db.ForeignKey ("tag.id")) #外键
    comments = db.Column (db.relationship ("Comment",backref = "movie"))
    moviefavs = db.Column (db.relationship ("Moviefav",backref = "movie"))

    def __repr__ (self):
        return "<Movie %r>" % self.title


class Preview (db.Model):
    '''
    上映预告模型
    '''
    __tablename__ = "preview"
    id = db.Column (db.Integer,primary_key = True,autoincrement = True)
    title = db.Column (db.String (255),unique = True)#标题
    logo = db.Column (db.String (255),unique = True)#封面
    add_time = db.Column (db.DateTime,index = True,default = datetime.datetime.utcnow ())

    def __repr__ (self):
        return "<Preview %s>" % self.title


class Comment (db.Model):
    '''
    电影评论模型
    '''
    __tablename__ = "comment"
    id = db.Column (db.Integer,primary_key = True,autoincrement = True)
    content = db.Column (db.Text)
    movie_id = db.Column (db.Integer,db.ForeignKey ("movie.id")) #外键
    user_id = db.Column (db.Integer,db.ForeignKey ("user.id")) #外键
    add_time = db.Column (db.DateTime,index = True,default = datetime.datetime.utcnow ())

    def __repr__ (self):
        return "<Comment %s>" % self.id


class Moviefav (db.Model):
    '''
    电影收藏模型
    '''
    __tablename__ = "moviefav"
    id = db.Column (db.Integer,primary_key = True,autoincrement = True)
    movie_id = db.Column (db.Integer,db.ForeignKey ("movie.id")) #外键
    user_id = db.Column (db.Integer,db.ForeignKey ("user.id")) #外键
    add_time = db.Column (db.DateTime,index = True,default = datetime.datetime.utcnow ())

    def __repr__ (self):
        return "<Moviefav %s>" % self.id
