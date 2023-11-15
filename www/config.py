import os

class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    #PWD = os.path.abspath(os.curdir)	
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/webdata.db'.format(PWD)
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig
}