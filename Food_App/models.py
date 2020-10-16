from datetime import datetime

from flask import current_app as app
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm.collections import attribute_mapped_collection

from . import db, login_manager


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    foods = db.relationship("Food", backref="users", lazy="dynamic")

    def get_confirmation_token(self, expires_sec=3600):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps(self.email).decode("utf-8")

    @staticmethod
    def confirm_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            email = s.loads(token)
        except:
            return False
        return email

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    morning = db.Column(db.String(40))
    afternoon = db.Column(db.String(40))
    night = db.Column(db.String(40))
    calories = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Food('{self.morning}','{self.afternoon}','{self.night}')"


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), nullable=False)
    provider_user_login = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(
        User,
        # This `backref` thing sets up an `oauth` property on the User model,
        # which is a dictionary of OAuth models associated with that user,
        # where the dictionary key is the OAuth provider name.
        backref=db.backref(
            "oauth",
            collection_class=attribute_mapped_collection("provider"),
            cascade="all, delete-orphan",
        ),
    )

    def __repr__(self):
        return f"OAuth('{self.token}','{self.user_id}','{self.provider_user_id}','{self.provider_user_login}')"
