#!/usr/bin/python3
# -*- coding: <encoding name> -*-

from flask import Blueprint,render_template,flash,redirect,url_for
from jobplus.forms import RegisterForm,LoginForm
from jobplus.models import db,User,Job,Company
from flask_login import login_user,logout_user,login_required


front = Blueprint('front',__name__)

@front.route('/')
def index():
    company_page = 1
    company_pagination = Company.query.order_by(Company.created_at.desc()).paginate(
            page = company_page,
            per_page=3,
            error_out=False
            )

    job_page = 1
    job_pagination = Job.query.order_by(Job.created_at.desc()).paginate(
            page = job_page,
            per_page=4,
            error_out=False
            )
    return render_template('index.html',company_pagination=company_pagination,job_pagination=job_pagination)


@front.route('/companyregister',methods=['GET','POST'])  
#注册路由，提供get,post方法
def companyregister():
      form = RegisterForm()  
      #引用flask-WTF,基类FlaskForm生成的对象。实现，pychon创建html的form。
      form.name.label = '企业名称' 
      #改变form.name.label 属性值（个人名称为企业名称）
      if form.validate_on_submit():  
          # validate_on_submit来自于，flask-WTF,提供的FlaskForm的方法中。
          company_user = form.create_user() 
          #将form从用户得到的数据，传给数据库。返回一个User对象。
          company_user.role = User.COMPANY #改变User对象role
          db.session.add(company_user) #更新数据
          db.session.commit()
          flash('注册成功，请登录','success') 
          return redirect(url_for('.login'))  #跳转到login 登录页面
      return render_template('companyregister.html',form=form)


#用户注册
@front.route('/userregister',methods=['GET','POST'])
def userregister():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，清登录','success')
        return redirect(url_for('.login'))
    return render_template('userregister.html',form=form)


#登录页面
@front.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # 使用flask-login模块，login_user函数（传入User对象，布尔值）实现注册
        login_user(user,form.remember_me.data)
        next = 'front.index'
        # Check if the user is banned
        if user.is_disable :
            flash('当前用户被禁用','info')
            return render_template('login.html',form=form)
        if user.is_admin:
            next = 'admin.index'
        if user.is_company:
            if user.company:
                next = 'front.index'
            else:
                next = 'company.profile'
        return redirect(url_for(next))
    return render_template('login.html',form=form)

#退出登录
@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录','success')
    return redirect(url_for('.index'))
