import os

basedir=os.path.abspath(os.path.dirname(__file__))

pg_user = 'admin'
pg_pass = 'admin'
pg_db = 'app'
pg_host = 'db'
pg_port = 5432

PROD_DB = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
VOLUME_PATH='/mnt/app'

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'rabbits-are-there'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
     #   'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = PROD_DB
