from flask import current_app as app
from .forms import RegistrationForm
from flask import render_template,url_for

@app.route("/")
@app.route("/home")
def home():
    return 'Hello'

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegistrationForm()
    return render_template('register.html',title='Register',form=form)
