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
neighboursarray = [[["B",2],["C",3]],[["A",2],["D",3]],[["A",3]],[["B",3],["E",4]],[["D",4]]]

class adminloginForm(FlaskForm):
    username = StringField("username")
    password = StringField("password")
    submit = SubmitField("submit")

class calculationForm(FlaskForm):
    startnode = StringField("startnode")
    endnode = StringField("endnode")
    submit = SubmitField("submit")

class admineditForm(FlaskForm):
    edge = StringField("node")
    weight = StringField("weight")
    submit = SubmitField("Confirm Edit")

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

def ingraph(graph,searchvalue):
    count = 0
    for x in graph:
        if x.value == searchvalue:
            return count
        else:
            count += 1
    return None


def define_graph(graph, inputarray, neighboursarray):
    graph2 = []
    for x in range(len(inputarray)):
        Node = inputarray[x]
        neighbours = neighboursarray[x]
        if ingraph(graph, Node) != None:
                this_node = graph[ingraph(graph,Node)]
        else:
            this_node = node(Node)
            graph.append(this_node)
            graph2.append(this_node.value)

        for neighbour in neighbours:
            if ingraph(graph, neighbour[0]) != None:
                this_neighbour = graph[ingraph(graph,neighbour[0])]
            else:
                this_neighbour = node(neighbour[0])
                graph.append(this_neighbour)
                graph2.append(this_neighbour.value)

            this_node.give_neighbour(this_neighbour)
            this_node.give_neighbour_weight(-int(neighbour[1]))

    return graph


graph = define_graph(graph, inputarray, neighboursarray)

def find_shortest(graph, startingnode, destination):
    answer = []
    startingnode = find_node(startingnode)
    Q = queue(len(graph)*10)
    Q.enqueue(startingnode,0)
    while Q.is_empty()==False:
        current = Q.dequeue()
        if current[0].checkfinal() == False:
            current[0].placeval = -current[1]
            current[0].final = True
            for neighbour in current[0].neighbours:
                num = current[0].getplaceofweight(neighbour)
                neighbour.placeval = current[0].placeval - int(current[0].weightofneighbours[num])
                neighbour.priority = neighbour.placeval
                print(f"Enqueue ={neighbour.value} from {current[0].value}")
                Q.enqueue(neighbour, -neighbour.priority)
            
            ## not used yet
            answer.append([current[0].value, current[0].placeval])
            ###
            if current[0].value == destination.upper():
                return current[0].placeval

def reset_nodes(graph):
    for node in graph:
        node.final = False
        node.placeval = 0
        node.priority = 0

def find_node(searchnode):
    count = 0
    for node in graph:
        count += 1
        if node.value == searchnode.upper():
            return node
    return None

def node_valid(inputarray, searchnode):
    for node in inputarray:
        if node == searchnode:
            return True
    return False

def node_location(inputarray, searchnode):
    count = 0
    for node in inputarray:
        count += 1
        if node == searchnode:
            return count
    return None

def change_weights(inputarray,neighboursarray,node1,node2,weight):
    node1location = node_location(inputarray, node1)
    node2location = node_location(inputarray, node2)

    for x in range(len(neighboursarray[node1location])):
        if neighboursarray[node1location][x] == node1:
            pass
    
    for x in range(len(neighboursarray[node2location])):
        if neighboursarray[node2location][x] == node2:
            pass

            
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
        form = admineditForm()
        if form.is_submitted():
            edges = form.edge.data
            edges = edges.split(">")
            weight = form.weight.data
            if node_valid(inputarray, node[0]) and node_valid(inputarray, node[1]):
                num1 = node_location(node[0])
                num2 = node_location(node[1])
                neighbours = neighboursarray[num1]
            else:
                return redirect(url_for("admin", form=form))
        else:
            return redirect(url_for("admin", form=form))
    else:
        return redirect(url_for("adminlogin"))

@app.route("/shortest", methods=["GET","POST"])
def shortest():
    form = calculationForm()
    nodes = inputarray
    if form.is_submitted():
        startingnode = form.startnode.data
        destination = form.endnode.data
        print(startingnode)
        print(destination)
        if startingnode == None or destination == None:
            return render_template("calculation.html",form=form, distance="Fill in both fields", nodes=nodes)
        elif startingnode == destination:
            return render_template("calculation.html",form=form, distance="Start and End must be Different", nodes=nodes)
        else:
            #try:
                print("attempting shortest")
                distance = find_shortest(graph,startingnode,destination)
                print("distance:",distance)
                reset_nodes(graph)
                return render_template("calculation.html",form=form, distance=distance, nodes=nodes)
            #except:
                return render_template("calculation.html",form=form, distance="Error", nodes=nodes)
    else:
        return render_template("calculation.html", form=form,distance=0, nodes=nodes)