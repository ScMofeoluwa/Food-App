from flask import current_app as app
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from . import bcrypt, db
from .email import send_email
from .forms import LoginForm, RegistrationForm
from .models import User


@app.route("/")
@app.route("/index")
def index():
    return "Hello"


@app.route("/home")
@login_required
def home():
    return render_template("home.html")


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
        token = user.get_confirmation_token()
        confirm_url = url_for("confirm_email", token=token, _external=True)
        html = render_template(
            "activate.html", confirm_url=confirm_url, username=user.username
        )
        subject = "Please confirm you email"
        send_email(user.email, subject, html)
        flash("A confirmation email has been sent to your email address", "success")
        return redirect(url_for("unconfirmed"))
    return render_template("register.html", title="Register", form=form)


@app.route("/confirm/<token>")
@login_required
def confirm_email(token):
    if current_user.confirmed:
        flash("Account already confirmed. Please login.", "success")
        return redirect(url_for("home")
    email = User.confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("home"))


@app.route("/unconfirmed")
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for("home"))
    return render_template("unconfirmed.html")


@app.route("/resend")
@login_required
def resend_confirmation():
    token = current_user.get_confirmation_token()
    confirm_url = url_for("confirm_email", token=token, _external=True)
    html = render_template(
        "activate.html", confirm_url=confirm_url, username=current_user.username
    )
    subject = "Please confirm you email"
    send_email(current_user.email, subject, html)
    flash("A confirmation email has been sent to your email address", "success")
    return redirect(url_for("unconfirmed"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if not user.confirmed:
                flash("Please confirm your account!", "warning")
                return redirect(url_for("unconfirmed"))
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check your mail and password", "danger")
    return render_template("login.html", title="Login", form=form)
