import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'baby'
    DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'cmps.db')