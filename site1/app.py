from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '743rhg928739jf11'

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Log In")

class RegisterForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    realname = StringField("RealName")
    city = StringField("City")
    submit = SubmitField("Sign Up")

# connect to db

conn = sqlite3.connect("userdata.db")

#checks if this username is already in use
def is_a_user(username):
    conn = sqlite3.connect("userdata.db")

    cur = conn.cursor()
    cur.execute(f"SELECT username FROM users WHERE username = '{username}'")

    length = len(cur.fetchall())

    return not length == 0


#checks if a this password is valid for a valid user
def valid_user_password(username, password):
    print("password:", password)
    conn = sqlite3.connect("userdata.db")

    cur = conn.cursor()
    cur.execute(f"SELECT password FROM users WHERE username = '{username}'")

    actual_password = ((cur.fetchall())[0][0])
    if str(actual_password) == password:
        return True
    else:
        return False

#checks if this password is valid
def valid_password(password):
    listpassword = list(password)
    for character in listpassword:
        if character == "\"" or character == "\\" or character == " ":
            return False
    return True 

#inserts a newly registered user into database
def insert_new_user(username, password, realname, city):
    conn = sqlite3.connect("userdata.db")
    now = datetime.now()
    conn.execute(f"INSERT INTO users (username, password, real_name, city, last_login, account_creation_date) VALUES ('{username}','{password}','{realname}','{city}','{now}','{now}');")
    conn.commit()

#updates the users login time
def update_user_login_time(username):
    conn = sqlite3.connect("userdata.db")
    now = datetime.now()

    conn.execute(f"UPDATE users SET last_login = '{now}' WHERE username = '{username}'")

    conn.commit()

#fetches database for admin view
def fetch_db():
    conn = sqlite3.connect("userdata.db")

    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users")

    value = cur.fetchall()
    return value

@app.route("/", methods=["GET", "POST"])
def login():
    entry_form = LoginForm()
    if entry_form.is_submitted():
        username = entry_form.username.data
        password = entry_form.password.data
        if username == "admin" and password == "admin":
            session["username"] = username
            return redirect(url_for("admin"))
        # implement admin stuff ^^^^
        elif is_a_user(username):
            if valid_user_password(username, password):
                session["username"] = username
                update_user_login_time(username)
                return redirect(url_for("home"))
            else:
                #flag wrong password to user
                print("incorrect password")
                return render_template("login.html", form=entry_form)
        else:
            #flag no username to user
            print("no user exists")
            return render_template("login.html", form=entry_form)
    else:
        return render_template("login.html", form=entry_form)
    
@app.route("/register", methods=["GET","POST"])
def register():
    entry_form = RegisterForm()

    if entry_form.is_submitted():
        username = entry_form.username.data
        password = entry_form.password.data
        realname = entry_form.realname.data
        city = entry_form.city.data
        if not is_a_user(username):
            if valid_password(password):
                insert_new_user(username, password, realname, city)
                session["username"] = username
                update_user_login_time(username)
                return redirect(url_for("home"))
            else:
                #flag bad password to user
                print("Bad password")
                return render_template("register.html", form=entry_form)
        else:
            #flag used username to user
            print("username already in use")
            return render_template("register.html", form=entry_form)
    else:
        return render_template("register.html", form=entry_form)

@app.route("/admin")
def admin():
    try:
        session["username"] == "admin"
        return render_template("logindata.html", accounts = fetch_db())
    except:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    del session["username"]
    return redirect(url_for("login"))

@app.route("/home")
def home():
    try:
        session["username"] != None
        return render_template("home.html")
    except:
        return redirect(url_for("login"))

# fixes:
# admin page - users last login doesnt update