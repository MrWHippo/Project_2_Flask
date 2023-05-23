from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
import sqlite3
from DijkstrasAlgorithmForWeb import queue, node


validadmins = [["admin1","goodpassword"],["admin2","admin2"]]

app = Flask(__name__)
app.secret_key = "njjrnbfjko39i"


graph = []

###
inputarray = ["A","B","C","D","E"]
neighboursarray = [["B","C"],["A","D"],["A"],["B","E"],["D"]]

class adminloginForm(FlaskForm):
    username = StringField("username")
    password = StringField("password")
    submit = SubmitField("submit")

class calculationForm(FlaskForm):
    startnode = StringField("start")
    endnode = StringField("end")
    submit = SubmitField("submit")


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


#### graph stuff

def ingraph(value):
    count = 0
    for x in graph:
        if x.value == value:
            return count
        else:
            count += 1
        return None


def define_graph(graph, inputarray, neighboursarray):
    graph2 = []
    for x in range(len(inputarray)):
        Node = inputarray[x]
        neighbours = neighboursarray[x]
        if ingraph(Node) != None:
                this_node = graph[ingraph(Node)]
        else:
            this_node = node(Node)
            graph.append(this_node)
            graph2.append(this_node.value)

        for neighbour in neighbours:
            if ingraph(neighbour[0]) != None:
                this_neighbour = graph[ingraph(neighbour[0])]
            else:
                this_neighbour = node(neighbour[0])
                graph.append(this_neighbour)
                graph2.append(this_neighbour.value)

            this_node.give_neighbour(this_neighbour)
            this_node.give_neighbour_weight(-int(neighbour[1]))

    return graph


graph = define_graph(graph, inputarray, neighboursarray)

def find_shortest(graph):
    Q = queue(len(graph)*10)
    Q.enqueue(graph[0],[0])
    while Q.is_empty()==False:
        current = Q.dequeue()
        if current[0].checkfinal() == False:
            current[0].placeval = -current[1]
            current[0].final = True
            for neighbour in current[0].neighbours:
                num = current[0].getplaceofweight(neighbour)
                neighbour.placeval = current[0].placeval - int(current[0].weightofneighbours[num])
                neighbour.priority = neighbour.placeval
                Q.enqueue(neighbour, -neighbour.priority)
            
            print(current[0].value,  current[0].placeval)


### roots

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

@app.route("/shortest", methods=["GET","POST"])
def shortest():
    form = calculationForm()
    if form.is_submitted():
        startingnode = form.startnode.data
        destination = form.endnode.data
        print(startingnode)
        print(destination)
        if startingnode == None or destination == None:
            return render_template("calculation.html",form=form, distance="Fill in both fields")
        elif startingnode == destination:
            return render_template("calculation.html",form=form, distance="Start and End must be Different")
        else:
            try:
                distance = find_shortest(graph,startingnode,destination)
                return render_template("calculation.html",form=form, distance=distance)
            except:
                return render_template("calculation.html",form=form, distance="Error")
    else:
        return render_template("calculation.html", form=form,distance=0)