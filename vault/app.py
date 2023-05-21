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
    password = PasswordField("password")
    confirmpassword = PasswordField("confirmpassword")
    accesscode = PasswordField("accesscode")
    submit = SubmitField("register")


@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.is_submitted():
        realname = form.realname.data
        username = form.username.data
        password = form.password.data
        password2 = form.confirmpassword.data
        accesscode = form.accesscode.data

        PRINT(realname)
        PRINT(username)
        PRINT(password)
        PRINT(password2)
        PRINT(accesscode)

        if realname == None or username == None or password == None or password2 == None or accesscode==None:
            print("Missing Field")
            return render_template("register.html", form=form)
        else:
            try:
                if users[username] != None:
                    user = True
            except:
                user = False
            if user == False:
                if password == password2:
                    if accesscode == ACCESS_CODE:
                        print("Access code correct, registering user.")
                        new_user = User(realname, username, password)
                        users[username] = new_user
                        print("User registed and redirected to login.")
                        return redirect(url_for("login"))
                    else:
                        print("Access code incorrect.")
                        return render_template("register.html", form=form)
                else:
                    print("Passwords dont match.")
                    return render_template("register.html", form=form)
            else:
                print(f"{username} is already in use.")
                return render_template("register.html", form=form)
    else:
        return render_template("register.html", form=form)



@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.is_submitted():
        username = form.username.data
        password = form.password.data
        user_info = users.get(username, None)
        if user_info is not None and user_info.password == password:
            print("login successful")
            session["username"] = username
            return redirect(url_for("welcome"))
        else:
            print("Login Failed")
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)

@app.route("/")
def welcome():
    username = session.get("username", None)
    if username is not None:
        try:
            realname = users[username].realname
        except:
            realname = "{couldn't get real name}"
        return render_template("welcome.html", realname=realname)
    else:
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect(url_for("login"))


def PRINT(value):
    print(value)

