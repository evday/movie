#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:09"
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField,StringField,PasswordField,FileField,TextAreaField
from wtforms.validators import DataRequired,EqualTo,Email,Regexp,ValidationError
from ..models import User
#会员注册表单
class RegisterForm (FlaskForm):
    name = StringField (
        label = "昵称",validators = [DataRequired ("请输入昵称!")],
        description = "昵称",render_kw = {"class":"form-control input-lg"}
    )
    email = StringField (label = "邮箱",validators = [DataRequired ("请输入邮箱!"),Email("邮箱格式不正确!")],
                         description = "邮箱",render_kw = {"class":"form-control input-lg","placeholder":"请输入邮箱!"}
                         )
    phone = StringField(
        label = "手机",
        validators = [DataRequired("请输入手机号!"),Regexp("1[3,4,5,7,8]\\d{9}",message = "手机格式不正确!")],
        description = "手机",
        render_kw = {"class":"form-control input-lg","placeholder":"请输入手机号!"}
    )
    pwd = PasswordField(
        label = "密码",
        validators = [DataRequired("请输入密码!")],description = "密码",
        render_kw = {"class":"form-control input-lg","placeholder":"请输入密码!"}
    )
    repwd = PasswordField (
        label = "确认密码",
        validators = [DataRequired ("请输入密码!"),EqualTo("pwd",message = "两次输入密码不一致!")],description = "确认密码",
        render_kw = {"class":"form-control input-lg","placeholder":"请输入密码!"}
    )
    submit = SubmitField(
        "提交",render_kw = {"class":"btn btn-lg btn-success btn-block"}
    )
    def validate_name(self,field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user:
            raise ValidationError("昵称已经存在!")
    def validate_email(self,field):
        email = field.data
        email = User.query.filter_by(email=email).count()
        if email:
            raise ValidationError("邮箱已经存在!")

    def validate_phone(self,field):
        phone = field.data
        phone = User.quert.filter_by(phone=phone).count()
        if phone:
            raise ValidationError("手机号已经存在!")

#会员登录表单
class LoginForm(FlaskForm):
    name = StringField(
        label = "账号",validators = [DataRequired("请输入账号!")],
        render_kw = {"class":"form-control","placeholder":"请输入账号!"}
    )
    pwd = PasswordField(
        label = "密码",validators = [DataRequired("请输入密码!")],
        render_kw = {"class":"form-control","placeholder":"请输入密码!"}
    )
    submit = SubmitField(
        "登录",render_kw = {"class":"btn btn-lg btn-primary btn-block"}
    )

#会员资料修改表单
class UserDetailForm(FlaskForm):
    name = StringField(
        label = "账号",validators = [DataRequired("请输入账号!")],
        render_kw = {"class":"form-control","placeholder":"请输入账号!"}
    )
    email = StringField(
        label = "邮箱",validators = [DataRequired("请输入邮箱!"),Email("邮箱格式不正确!")],
        render_kw = {"class":"form-control","placeholder":"请输入邮箱!"}
    )
    phone = StringField(
        label = "手机",validators = [DataRequired("请输入手机号码!"),Regexp("1[3,4,5,7,8]\\{9}",message = "手机格式不正确!")],
        render_kw = {"class":"form-control","placeholder":"请输入手机号!"}
    )
    face = FileField(
        label = "头像",validators = [DataRequired("请上传头像!")]
    )
    info = TextAreaField(
        label = "简介",validators = [DataRequired("请输入简介!")],
        render_kw = {"class":"form-control","rows":10}
    )
    submit = SubmitField("确认修改!",render_kw = {"btn btn-success"})

#会员密码修改
class PwdForm(FlaskForm):
    old_pwd = StringField(label = "旧密码",validators = [DataRequired("请输入旧密码!")],
                          description = "旧密码",render_kw = {"class":"form-control","placeholder":"请输入旧密码"})
    new_pwd = StringField(label = "新密码",validators = [DataRequired("请输入新密码!")],
                          description = "新密码",render_kw = {"class":"form-control","placeholder":"请输入新密码"})
    submit = SubmitField("提交",render_kw = {"class":"form-control"})


