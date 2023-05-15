from flask import Flask , redirect, url_for , request

app = Flask(__name__)

@app.route("/")
def index():
    return '''<h1>Index Page</h1>
                <p>Hello world!</p>'''

@app.route("/goodbye")
def goodbyePage():
    return '''<h1>Goodbye Page</h1>
            <p>Goodbye world!</p>'''

@app.route("/greet/<name>")
def greet(name):
    nameWithCap = name.title()
    return f"<h1>Hello, {nameWithCap}.</h1>"

#url redirects

@app.route("/admin")
def hello_admin():
    return '<h1>Hello Admin</h1>'

@app.route("/guest/<guest>")
def hello_guest(guest):
    return f'<h1>Hello {guest} as Guest</h1>'

@app.route("/user/<name>")
def hello_user(name):
    if name == 'admin':
        return redirect(url_for("hello_admin"))
    else:
        return redirect(url_for("hello_guest", guest = name))
    
# request
    
@app.route("/analyze")
def analyzeRequest():
    print("Headers: ", request.headers)
    print("Args: ", request.args)
    return '''<h1>Check Flask console for details.</h1>'''