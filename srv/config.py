
import os
import sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
load_dotenv(sys.path[0])

class Config:
    # Database related config
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")

    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://{}:{}@{}:{}/{}?sslmode=disable".format(
            DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
        )
    )
    SQLALCHEMY_ENABLE_POOL_PRE_PING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5
        }
    }

    UTC_OFFSET = 8

    # Mail related config
    MAIL_SERVER = os.environ.get("MAIL_HOST")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = False
    TESTING = False

    #celery config
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    BROKER_URL = os.environ.get('REDIS_URL', "redis://{host}:{port}/0".format(host=REDIS_HOST, port=str(REDIS_PORT)))
    CELERY_RESULT_BACKEND = BROKER_URL
