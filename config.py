import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'inspiration.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ["inspiration_secret_key"]
    LOGIN = os.environ["inspiration_login"]
    PASSWORD = os.environ["inspiration_password"]


class HerokuConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgres://ulmwdexsbnijrv:add169d1ace2d010785b983030da50cf07e1eb512420d66448ab5950c3f48608@ec2-54-221-214-3.compute-1.amazonaws.com:5432/d2ftce74vj3d2i"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ["inspiration_secret_key"]
    LOGIN = os.environ["inspiration_login"]
    PASSWORD = os.environ["inspiration_password"]
