from flask import Flask, render_template
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY']='tb3njt39h8fi20'

class LoginForm(FlaskForm):
    username = StringField("Username")
    submit = SubmitField("Log In")

@app.route("/", methods=["GET","POST"])
def login():
    entry_form= LoginForm()
    return render_template("login.html", form=entry_form)


