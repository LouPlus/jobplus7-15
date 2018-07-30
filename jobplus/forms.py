#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField 
from wtforms.validators import Required,Length,EqualTo,Email
from jobplus.models import db,User

class RegisterForm():
    username = StringField('用户名',validators=[Required(),Length(3,24)])
    email = StringField('邮件',validators=[Required(),Email()])
    password = PasswordField('密码',validators=[Required(),Length(6,24)])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    submit = SubmitField()

    def validate_username(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('名字已存在')


    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

                           
    def create_user(self):   #在数据中创建User
        user = User(name=self.username.data,
                    email=self.email.data,
                    password=self.password.data) #将form 相应数据传入
        db.session.add(user)
        db.session.commit()
        return user
