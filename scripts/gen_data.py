#!/usr/bin/python3
# -*- coding: utf-8 -*-

# !!! IMPORTANT !!!
# Must create database in mysql with 'CREATE DATABASE jobplus CHARACTER utf8;'
# Otherwise will cause Warning 'Incorrect string value'
# !!! IMPORTANT !!!

# Usage: in flask shell:
#    >>> from scripts.gen_data import run
#    >>> run()

import os
from jobplus.models import db, User, Job, Delivery
from collections import namedtuple
from random import randint
from faker import Faker

tuser = namedtuple('tuser',['username','email','password','role'])

tuserlist = [
#Administration account
tuser('admin','admin@jobplus.com','jobplus',30),
#Company account
tuser('company','company@jobplus.com','jobplus',20),
#Standard user
tuser('test','test@jobplus.com','jobplus',10)
]

fake = Faker('zh-CN')

def iter_users():
    for tuser in tuserlist:
        yield User(
            username=tuser.username,
            email=tuser.email,
            password=tuser.password,
            role=tuser.role
        )

def iter_jobs():
    company_user = User.query.filter_by(username='company').first()
    for i in range(5):
        yield Job(
                name = fake.job(),
                low = randint(6000,10000),
                high = randint(10001,20000),
                tags = fake.color_name(),
                experience = fake.text(max_nb_chars=30),
                description = fake.text(max_nb_chars=100),
                company=company_user
                )

def iter_delivs():
    deliv_user = User.query.filter_by(username='test').first()
    deliv_comp = User.query.filter_by(username='company').first()
    for job in Job.query.filter_by(company_id=deliv_comp.id).all():
        yield Delivery(
                job_id=job.id,
                user_id=deliv_user.id,
                company_id=deliv_comp.id
                )

def run():
    for user in iter_users():
        db.session.add(user)

    for job in iter_jobs():
        db.session.add(job)

    for deliv in iter_delivs():
        db.session.add(deliv)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
