from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField

app = Flask(__name__)
app.secret_key = "n238u2ifoid3opPo"

ACCESS_CODE = "42"

users = {}

class User:
    def __init__(self, realname, username, password):
        self.realname = realname
        self.username = username
        self.password = password

class LoginForm(FlaskForm):
    username= StringField("username")
    password = PasswordField("password")
    submit = SubmitField("submit")

class RegisterForm(FlaskForm):
    realname = StringField("realname")
    username = StringField("username")
    password = StringField("password")
    password2 = PasswordField("confirm_password")
    accesscode = PasswordField("access_code")


