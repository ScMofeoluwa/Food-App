from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id:int):
    return User.query.get(user_id)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(40),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    foods = db.relationship('Food',backref='users',lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
    

class Food(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    morning = db.Column(db.String(40))
    afternoon = db.Column(db.String(40))
    night = db.Column(db.String(40))
    calories = db.Column(db.Integer,default=0)
    date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Food('{self.morning}','{self.afternoon}','{self.night}')"