import os

class Config(object):
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or '8e422c119fcc0bdb1e78777d4febaaf7'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'flask'
