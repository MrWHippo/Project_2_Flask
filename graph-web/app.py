from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
import sqlite3
from 


validadmins = [["admin1","goodpassword"],["admin2","admin2"]]

app = Flask(__name__)
app.secret_key = "njjrnbfjko39i"

class adminloginForm(FlaskForm):
    username = StringField("username")
    password = StringField("password")
    submit = SubmitField("submit")


@app.route("/adminlogin", methods=["GET","POST"])
def adminlogin():
    form = adminloginForm()
    if form.is_submitted():
        username = form.username.data
        password = form.password.data

        if is_admin(username):
            if correctpassword(username, password):
                print("Admin entered")
                return render_template("admin.html")
            else:
                print("Incorrect Password")
                return render_template("adminlogin.html", form=form)
        else:
            print("Incorrect username")
            return render_template("adminlogin.html", form=form)
    else:
        return render_template("adminlogin.html", form=form)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect(url_for("home"))

@app.route("/admin")
def admin():
    username = session.get("username", None)
    if username is not None:
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("adminlogin"))
    
@app.route("/shortest")
def shortest():
    return render_template("calculation.html")

def is_admin(username):
    for user in validadmins:
        if username == user[0]:
            print("user found")
            return True
    print("No user found")
    return False

def correctpassword(username, password):
    for user in validadmins:
        if username == user[0]:
            print("User found")
            if password == user[1]:
                print("password correct")
                return True
            else:
                print("password incorrect")
                return False
    print("No user found")
    return False