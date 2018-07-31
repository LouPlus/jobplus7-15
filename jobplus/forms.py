#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField
from wtforms.validators import Required,Length,EqualTo,Email,URL
from jobplus.models import db,User,Company

class RegisterForm(FlaskForm):
    name = StringField('用户名',validators=[Required(),Length(3,24)])
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
        user = User(username=self.name.data,
                    email=self.email.data,
                    password=self.password.data) #将form 相应数据传入
        db.session.add(user)
        db.session.commit()
        return user

class AddUserForm(FlaskForm):
    real_name = StringField('姓名', validators=[Required(), Length(2,20)])
    email = StringField('邮箱', validators=[Required(),Email()])
    phone = StringField('手机号码', validators=[Required(), Length(11,11)])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('完成')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


    def create_user(self):
        user = User(real_name=self.real_rname.data,
                    email=self.email.data,
                    password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self,user):
        self.populate_boj(user)
        db.session.add(user)
        db.session.commit()
        return user


class AddCompanyForm(FlaskForm):
    name = StringField('企业名称', validators=[Required(), Length(3)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    site = StringField('企业网站', validators=[Required, URL()])
    description = StringField('一句话简介', validators=[Required(), Length(max=100)])
    submit = SubmitField('完成')

    def validate_name(self, field):
        if Company.query.filter_by(name=field.data).first():
            raise ValidationError('公司已经存在')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

    def create_company(self):
        user = User(
            email=self.email.data,
            password=self.password.data,
            role=20
        )
        company = Company(name=self.name.data,
                       email=self.email.data,
                       site=self.site.data,
                       description=self.description.data,
                       user=user
                       )
        db.session.add(user)
        db.session.add(company)
        db.session.commit()
        return user, company

    def update_company(self,company):
        company.user.email = self.email.data
        company.user.password = self.password.data
        company.name = self.name.data
        company.email = self.email.data
        company.site = self.site.data
        company.description = self.description.data
        db.session.add(company)
        db.session.commit()
        return company
