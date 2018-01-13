#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-07,17:10"
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,ValidationError

from ..models import Admin

class LoginForm(FlaskForm):
    """
    管理员登录表单
    """
    account = StringField(
        label = "账号",
        validators = [
            DataRequired("请输入账号！")
        ],
        description = "账号",
        render_kw = {
            "class":"form-control",
            "placeholder":"请输入账号！"
        }
    )
    pwd = PasswordField(
        label = "密码",
        validators = [
            DataRequired("请输入密码！")
        ],
        description = "密码",
        render_kw = {
            "class":"form-control",
            "placeholder":"请输入密码！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw = {
            "class":"btn btn-primary btn-block btn-flat"
        }
    )
    def validate_account(self,field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if not admin:
            raise ValidationError("账号不存在！")

class TagForm(FlaskForm):
    name = StringField(
        label = "名称",
        validators = [DataRequired("请输入标签！")],
        description = "标签",
        render_kw = {
            "class":"form-control",
            "id":"input_name",
            "placeholder":"请输入标签名称！",
        }
    ),
    pwd = SubmitField(
        "添加",
        render_kw = {
            "class":"btn btn-primary"
        }
    )
