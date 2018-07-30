#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class Base(db.Model):
    '''所有model的基类，默认添加了时间戳
    继承该类获取模块的使用，避免重复创建和更新
    '''
    # 表示不把此类作为Model类即不创建此类的表
    __abstract__ = True
    # 设置了 default 和 onupdate 这俩个时间戳都不需要自己去维护
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)


'''用户表和工作表的关联，投递职位，多对多'''
user_job = db.Table(
    'user_job',
    db.Column('user_id', db.Integer, db.ForeignKey('user_id', ondeleta='CASCADE')),
    db.Column('job_id', db.Integer, db.ForeignKey('job_id', ondeleta='CASCADE'))
)


class User(Base, UserMixin):
    __tablename__ = 'user'
    """管理员，求职者，企业"""

    USER = 10
    COMPANY = 20
    ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    phone = db.Column(db.String(11))
    password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=USER)     # 默认求职者用户
    resume = db.Column(db.String(64), unique=True, index=True, nullable=False)   # 用户简历
    upload_resume = db.Column(db.String(64))                           # 上传简练，string存储地址
    link_jobs = db.relationship('Job', secondary=user_job)
    # User status (is disable?), True for Disbale, False for Enable
    is_disable = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def _password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def admin(self):
        return self.role == self.ADMIN

    @property
    def company(self):
        return self.role == self.COMPANY


class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True, unique=True)
    slug = db.Column(db.String(24), nullable=False, index=True, unique=True)
    logo = db.Column(db.String(64), nullable=False)
    # 网址
    site = db.Column(db.String(64), nullable=False)
    # 联系方式
    contact = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(24), nullable=False)
    # 地址
    location = db.Column(db.String(24), nullable=False)
    # 一句话的描述
    description = db.Column(db.String(100))
    # 关于，公司详情描述
    about = db.Column(db.String(1024))
    # 标签
    tags = db.Column(db.String(128))
    # 公司技术站
    stack = db.Column(db.String(128))
    # 团队介绍
    team = db.Column(db.String(256))
    # 公司福利
    welfare = db.Column(db.String(256))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondeleta='SET NULL'))
    user = db.relationship('User', uselist=False, backref=db.backref('company', uselist=False))

    def __repr__(self):
        return '<Company {}>'.format(self.name)


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    # 职位名称
    name = db.Column(db.String(24))
    # 岗位提供薪酬范围
    low = db.Column(db.Integer, nullable=False)
    high = db.Column(db.Integer, nullable=False)
    # 职位标签
    tags = db.Column(db.String(128))
    # 经验
    experience = db.Column(db.String(32))
    # 学历
    degree = db.Column(db.String(32))
    # 职位类型，全、兼、实习等
    types = db.Column(db.Boolean, default=True)
    # 招聘状态，在招或下架
    up = db.Column(db.Boolean, default=True)
    # 被查看次数
    views = db.Column(db.Integer, default=0)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondeleta='CASCADE'))
    company = db.relationship('Company', uselist=False)


class Status(Base):
    __tablename__ = 'status'
    # 审核
    REVIEW = 1
    # 通知拒绝
    REFUSE = 2
    # 同意面试
    ARGEE = 3

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondeleta='SET NULL'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondeleta='SET NULL'))
    status = db.Column(db.SmallInteger, default=REVIEW)
    # 企业回应
    response = db.Column(db.String(256))
