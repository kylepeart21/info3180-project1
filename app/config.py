import os
class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:061502kp@localhost/info3180_db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False