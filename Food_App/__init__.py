from config import Config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
mail = Mail()
login_manager.login_view = "login"
login_manager.login_message_category = "danger-alert"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes
        from .oauth import facebook_blueprint, google_blueprint, twitter_blueprint

        app.register_blueprint(facebook_blueprint, url_prefix="/login")
        app.register_blueprint(google_blueprint, url_prefix="/login")
        app.register_blueprint(twitter_blueprint, url_prefix="/login")

        return app
