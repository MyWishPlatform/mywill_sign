import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = False
    SECRET_KEY = 'etinoieanwitnftfenirnntfr389323298tnrie'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/lastwill_sign'
