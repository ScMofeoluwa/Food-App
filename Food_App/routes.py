from flask import current_app as app
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from Food_App import bcrypt, db

from .forms import LoginForm, RegistrationForm
from .models import User


@app.route("/")
@app.route("/index")
def index():
    return "Hello"


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("login.html", title="Login", form=form)
