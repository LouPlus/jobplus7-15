#!usr/bin/python3
# -*- condig:utf-8 -*-

from flask import Flask,render_template
#from flask_migrate import Migrate
#from flask_login import LoginManager

from jobplus.config import configs
#from jobplus.models import db,User #按需求添加修改 

def register_extensions(app): #flask所需插件注册
    pass
'''
    db.init_app(app)
    Migrate(app,db)
    login_manager = LoginManager()
'''
    #按照个人使用添加完善

def register_blueprints(app):
    from .handlers import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

def register_error_handlers(app):
    '''因为使用接口通信，出错也返回json数据'''
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error/404.html'),404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('error/500.html'),500


def create_app(config):
    '''APP工厂'''
    app = Flask(__name__)

    if isinstance(config,dict):      
        app.config.update(config)
    else:
        app.config.from_object(configs.get(config,None))

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)

    return app
