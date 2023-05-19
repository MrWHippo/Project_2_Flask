from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from random import randint


app = Flask(__name__)
app.config['SECRET_KEY']='278926fbejfj29'

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

def GetAccountIndex(username):
    count = 0
    for i in accounts:
        if i[0] == username:
            return count
        count += 1

def MakeAccountNumber():
    account_number = NumberGenerator()
    while ValidNewAccountNumber(account_number) == False:
        account_number = NumberGenerator()
    return account_number

def NumberGenerator():
    num = []
    while len(num) < 6:
        num.append(str(randint(0,9)))
    num = "".join(num)
    return int(num)


def ValidNewAccountNumber(account_number):
    for i in accounts:
        if i[2] == account_number:
            return False
    return True

def writeaccount(username, password, account_number, funds):
    file = open("accounts.txt", "a")
    file.write(f"/{username},{password},{account_number},{funds}")
    file.close()

def readaccounts():
    file = open("accounts.txt","r")
    contents = file.read()
    file.close()
    print(contents)
    accounts = contents.split("/")
    print(accounts)
    for x in range(len(accounts)):
        accounts[x] = accounts[x].split(",")
    print(accounts)
    return accounts

accounts = readaccounts()  


@app.route("/", methods=["GET", "POST"])
def login():
    entry_form=LoginForm()

    if entry_form.is_submitted():
        username = entry_form.username.data
        password = entry_form.password.data
        if username == "admin":
            return render_template("admin.html", accounts=accounts)
        if username=="":
            return render_template("login.html", form=entry_form)
        elif IsRealUser(username):
            if password == UserPassword(username):
                index = GetAccountIndex(username)
                return render_template("home.html", username=username, funds= accounts[index][3])
            else:
                print("Incorrect password")
                print(accounts)
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
        password = entry_form.password.data
        if username != "" and password != "":
            account_number = MakeAccountNumber()
            funds = 0
            accounts.append([username, password, account_number, funds])
            writeaccount(username, password, account_number, funds)
            print("New account created")
            return render_template("home.html", username=username, funds=0.00)
        else:
            return render_template("login.html", form=entry_form)
        
    else:
        return render_template("login.html", form=entry_form)







