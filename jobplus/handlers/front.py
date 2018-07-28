#!/usr/bin/python3
# -*- coding: <encoding name> -*-

from flask import Blueprint,render_template,flash,redirect,url_for
from jobplus.forms import RegisterForm
from jobplus.models import db,User

front = Blueprint('front',__name__,url_prefix='/')

@front.route('/')
def index():
    return render_template('index.html')


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
          company_user.role = User.ROLE_COMPANY #改变User对象role
          db.session.add(company_user) #更新数据
          dv.session.commit()
          flash('注册成功，请登录','success') 
          return redirect(url_for('.login'))  #跳转到login 登录页面
      return render_template('companyregister.html',form=form)

