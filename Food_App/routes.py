from flask import current_app as app
from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user

from .forms import RegistrationForm
from .models import User


@app.route("/")
@app.route("/index")
def index():
    return "Hello"


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form)
