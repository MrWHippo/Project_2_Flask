from flask import Flask, redirect, url_for
from math import modf

app= Flask(__name__)

@app.route("/")
def main():
    return "<h1>Hello there</h1>"

@app.route("/admin/<password>")
def admin(password):
    if password == "password":
        return '<h1>Access Granted</h1>'
    elif password == "123456":
        return '<h1>Enter Password in URL</h1>'
    else:
        return '<h1>Access Denied</h1>'
    
@app.route("/guest/<name>")
def guest(name):
    if name == "admin":
        return redirect(url_for("admin", password = "123456"))
        pass
    else:
        return f'<h1>Hello {name}.</h1>'
    
@app.route("/issquare/<num>")
def isSquare(num):
    x, y = modf(int(num)**(1/2))
    if x == 0:
        y = int(y)
        return f'<h1>The square root of {num} is {y}</h1>'
    else:
        return f'<h1>{num} is not a square number, but {int(y**2)} is.'
    
@app.route("/isprime/<num>")
def isPrime(num):
    num = int(num)
    if is_prime(num) == True:
        return f'<h1>{num} is Prime</h1>'
    else:
        nextPrime = next_prime(num)
        return f'<h1>{num} is not Prime, But {nextPrime} is.</h1>'

def is_prime(n):
  for i in range(2,n):
    if (n%i) == 0:
      return False
  return True

def next_prime(n):
    num = n+1
    while is_prime(num) == False:
        num+=2
    return num

