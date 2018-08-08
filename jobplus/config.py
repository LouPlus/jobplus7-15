#!/usr/bin/python3
# -*- coding: utf8 -*-

"""jobplus.config
jobplus config file

    usage:

    from jobplus.config import configs
    def create_app(config):
        ...
        app.config.from_object(configs.get(config))
        ...

    config can be "development", "production", "testing"
"""

import os

class BaseConfig(object):
    SECRET_KEY = 'jobplus7-15'
    INDEX_PER_PAGE = 9
    ADMIN_PER_PAGE = 15

class DevConfig(BaseConfig):
    """Development Environment
    """

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:root@localhost:3306/jobplus?charset=utf8'
    TEMPLATES_AUTO_RELOAD = True

class ProductConfig(BaseConfig):
    """Production Environment
    """
    DEBUG = False

    #database file uri
    path = os.path.join(os.getcwd(),'jobplus.db').replace('\\','/')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://%s?charset=utf8' % path

class TestConfig(BaseConfig):
    pass

configs = {
    'development': DevConfig,
    'production': ProductConfig,
    'testing': TestConfig
}
