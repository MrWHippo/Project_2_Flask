from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
import sqlite3

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
                        print("Access code correct, registering user")
                        insert_user(realname, username, password)
                        print("User registed and redirected to login")
                        return redirect(url_for("login"))
                    else:
                        print("Access code incorrect.")
                        return render_template("register.html", form=form)
                else:
                    print("Passwords do not match")
                    return render_template("register.html", form=form)
            else:
                print(f"{username} is already in use")
                return render_template("register.html", form=form)
    else:
        return render_template("register.html", form=form)



@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.is_submitted():
        username = form.username.data
        password = form.password.data
        user_info = get_user_info(username)
        if username == "admin" and password == "admin":
            print("Admin viewing db")
            session["username"] = username
            #print_db()
            return render_template("admin.html", accounts= fetch_db())
        if user_info is not None and user_info[1] == password:
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
            realname = get_user_info(username)[0]
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


def insert_user(realname, username, password):
    conn = sqlite3.connect("users.db")
    print("Accessing Database")
    print("Adding User to Database")
    conn.execute(f"INSERT INTO USERS (REALNAME,USERNAME,PASSWORD) \
                 VALUES ('{realname}','{username}','{password}')")
    conn.commit()
    print(f"{username} added")
    conn.close()

def get_user_info(username):
    conn = sqlite3.connect("users.db")
    print("Accessing Database")
    print("Fetching User")
    userinfo = conn.execute(f"SELECT realname,password from USERS where username='{username}'")
    try:
        for value in userinfo:
            realname = value[0]
            password = value[1]
        conn.close()
        print("User Found")
        return [realname, password]
    except:
        conn.close()
        return None

def is_already_a_user(username):
    conn = sqlite3.connect("users.db")
    print("Accessing Database")
    print("Searching for User")
    userinfo = conn.execute(f"SELECT realname,password from USERS where username='{username}'")
    for value in userinfo:
        conn.close()
        print("User Found")
        return True
    conn.close()
    print("No user")
    return False

def print_db():
    conn = sqlite3.connect("users.db")
    print("printing db")
    userinfo = conn.execute("SELECT realname, username, password from USERS")
    for value in userinfo:
        print("---------------------------")
        print("Realname = ", value[0])
        print("Username = ", value[1])
        print("Password = ", value[2])
    conn.close()

def fetch_db():
    userinfo_array = []
    conn = sqlite3.connect("users.db")
    print("Fetching db")
    userinfo = conn.execute("SELECT realname, username, password from USERS")
    for account in userinfo:
        userinfo_array.append(account)
    conn.close()
    print("db fetched and returned")
    return userinfo_array

        