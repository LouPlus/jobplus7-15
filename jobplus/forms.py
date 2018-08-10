#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField
from wtforms.validators import Required,Length,EqualTo,Email,URL
from jobplus.models import db,User,Company,Job


#注册表单
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

#登录表单
class LoginForm(FlaskForm):
    email = StringField('邮件', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self,field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册')

    def validate_password(self,field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


#求职者，个人信息表
class UserProfileForm(FlaskForm):
    real_name = StringField('姓名')
    email = StringField('邮箱',validators=[Required(), Email()])
    password = PasswordField('密码（不填写保持不变）')
    phone = StringField('手机号')
   # work_years = IntegerField('工作年限')
    resume = StringField('简历地址')
    submit = SubmitField('提交')

    def validate_phone(self,field): #电话验证器
        phone = field.data
        if phone[:2] not in ('13','15','18') or len(phone) !=11 :
            raise ValidationError('请输入有效的手机号')
    
    #要查看User对象的属性
    def updata_profile(self,user): #传入User对象，将相应数据写入，传入数据库
        user.real_name = self.real_name.data
        user.email = self.email.data
        if self.password.data :
            user.password = self.password.data
        user.phone = self.phone.data
       # user.work_years = self.work_years.data
        user.resume = self.resume.data
        db.session.add(user)
        db.session.commit()


#公司信息表
class CompanyProfileForm(FlaskForm):
    username = StringField('企业名称')
    email = StringField('邮件',validators=[Required(),Email()])
    password = PasswordField('密码（不填写保持不变）')
    location = StringField('地址',validators=[Length(0,64)])
    contact = StringField('公司电话')
    site = StringField('公司网站',validators=[Length(0,64)])
    logo = StringField('Logo')
    description = StringField('一句话描述',validators=[Length(0,100)])
    about = TextAreaField('公司详情',validators=[Length(0,1024)])
    submit = SubmitField('提交')

    def validate_contact(self,field):
        contact = field.data
        if contact[:2] not in ('13','15','18') or len(contact) !=11:
            raise ValidationError('请输入有效的手机号')

    def updated_profile(self,user):
        user.username = self.username.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data

        if user.company:
            company_detail = user.company
        else :
            company_detail = Company()
            company_detail.user_id = user.id
        self.populate_obj(company_detail)

        db.session.add(user)
        db.session.add(company_detail)
        db.session.commit()



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
        user = User(username=self.real_name.data,
                    real_name=self.real_name.data,
                    email=self.email.data,
                    phone=self.phone.data,
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
    site = StringField('企业网站', validators=[Required(), URL()])
    description = StringField('一句话简介', validators=[Required(), Length(max=100)])
    submit = SubmitField('完成')

    def validate_name(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('公司名称已经存在')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

    def create_company(self):
        user = User(
            username=self.name.data,
            email=self.email.data,
            password=self.password.data,
            role=20
        )
        company = Company(
                       email=self.email.data,
                       site=self.site.data,
                       description=self.description.data,
                       user=user,
                       logo='',
                       location=''
                       )
        db.session.add(user)
        db.session.add(company)
        db.session.commit()
        return user, company

    def update_company(self,company):
        company.user.email = self.email.data
        company.user.password = self.password.data
        company.user.username = self.name.data
        company.email = self.email.data
        company.site = self.site.data
        company.description = self.description.data
        db.session.add(company)
        db.session.commit()
        return company

class AddJobForm(FlaskForm):
    name = StringField('职位名称', validators=[Length(3)])
    low = IntegerField('最低薪酬', validators=[Required()])
    high = IntegerField('最高薪酬', validators=[Required()])
    experience = StringField('经验要求', validators=[Length(max=32)])
    description = StringField('职位描述', validators=[Length(max=128)])
    degree = StringField('职位学历要求', validators=[Length(max=32)])
    submit = SubmitField('提交')

    def create_job(self,company):
        job = Job()
        self.populate_obj(job)
        job.company=company
        db.session.add(job)
        db.session.commit()
        return job

    def update_job(self,job):
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
        return job
