from os import environ, path
from dotenv import load_dotenv


basedir = path.dirname(path.abspath(__file__))
load_dotenv(path.join(basedir, ".env"), verbose=True)


class Config:
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_OAUTH_CLIENT_ID = environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    FACEBOOK_OAUTH_CLIENT_ID = environ.get("FACEBOOK_OAUTH_CLIENT_ID")
    FACEBOOK_OAUTH_CLIENT_SECRET = environ.get("FACEBOOK_OAUTH_CLIENT_SECRET")
    TWITTER_OAUTH_CLIENT_KEY = environ.get("TWITTER_OAUTH_CLIENT_KEY")
    TWITTER_OAUTH_CLIENT_SECRET = environ.get("TWITTER_OAUTH_CLIENT_SECRET")

class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"
