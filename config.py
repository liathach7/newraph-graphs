import os
from datetime import timedelta

basedir=os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SESSION_TYPE='sqlalchemy'
    PERMANENT_SESSION_LIFETIME=timedelta(days=3)
    #SESSION_SQLALCHEMY=db