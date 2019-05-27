import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'inspiration.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ["inspiration_secret_key"]
    LOGIN = os.environ["inspiration_login"]
    PASSWORD = os.environ["inspiration_password"]