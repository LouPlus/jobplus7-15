#!/usr/bin/python3
# -*- condig:utf-8 -*-

from flask import Flask,render_template
from flask_migrate import Migrate
from flask_login import LoginManager

from jobplus.config import configs
from jobplus.models import db,User #按需求添加修改 

def register_extensions(app): #flask所需插件注册
    #flask_sqlalchemy 
    db.init_app(app)
    
    #flask_migrate 
    Migrate(app,db)

    #flask_login 
    #使用flask_login插件，LoginManager类，实现注册
    login_manager = LoginManager()
    #调用.init_app方法初始化app
    login_manager.init_app(app)
    #使用user_loader装饰器注册一个函数，用来告诉flask_login,如何加在用户
    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)
    #LoginManager类.login_view设置登录的路由
    #当用flask_login提供的login_required 装饰器保护一个路由时，用户未登会被定向到 login_view 指定的页面。
    login_manager.login_view = 'front.index'

def register_blueprints(app):
    from .handlers import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)


def register_error_handlers(app):
    '''因为使用接口通信，出错也返回json数据'''
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('error/500.html'), 500


def create_app(config):
    '''APP工厂'''
    app = Flask(__name__)

    if isinstance(config, dict):
        app.config.update(config)
    else:
        app.config.from_object(configs.get(config, None))

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)

    return app
