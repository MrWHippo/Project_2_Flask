from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


app = Flask(__name__)
app.config['SECRET_KEY']='278926fbejfj29'


accounts = []
accountNumberGen = 1000000

class LoginForm(FlaskForm):
    username= StringField("Username")
    password= StringField("Password")
    submit = SubmitField("Log In")

class SignupForm(FlaskForm):
    username= StringField("Username")
    password= StringField("Password")
    submit = SubmitField("Sign Up")

def IsRealUser(username):
    for i in accounts:
        if i[0] == username:
            return True
    return False
        
def UserPassword(username):
    for i in accounts:
        if i[0] == username:
            return i[1]
    return False

@app.route("/", methods=["GET", "POST"])
def login():
    entry_form=LoginForm()

    if entry_form.is_submitted():
        username = entry_form.username.data
        password = entry_form.password.data
        if username=="":
            return render_template("login.html", form=entry_form)
        elif IsRealUser(username):
            if password == UserPassword(username):
                return render_template("home.html")
            else:
                print("Incorrect password")
                return render_template("login.html", form=entry_form)
        else:
            print("No user exists")
            return render_template("login.html", form=entry_form)
    else:
        return render_template("login.html", form=entry_form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    entry_form= SignupForm()

    if entry_form.is_submitted():
        username = entry_form.username.data
        password = entry_form.username.data
        if username != "" and password != "":
            accountnum = accountNumberGen
            accountNumberGen += 1
            funds = 0
            accounts.append([username, password, accountnum, funds])
            print("New account created")
            return render_template("home.html")
        else:
            return render_template("login.html", form=entry_form)
        
    else:
        return render_template("login.html", form=entry_form)
