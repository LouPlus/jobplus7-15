import os
from jobplus.models import db, User

username = 'admin'
password = 'jobplus'

def iter_admin():
    yield User(
            username=username,
            email='admin@jobplus.com',
            password=password,
            role=30,
        )

def run():
    for admin in iter_admin():
        db.session.add(admin)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
