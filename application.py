import os

import json
from models import *
import requests

from flask import Flask, session, render_template, redirect, url_for,request, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
@login_required
def index():
    return render_template("main.html",name = session["username"])

@app.route("/register_user")
def register_user():
    return render_template("register_user.html")

@app.route("/register", methods=["POST","GET"])
def register():
    #registrar usuario
    username = request.form.get('username')
    password = request.form.get('password')
    repassword = request.form.get('repassword')
    if password != repassword:
        return render_template('error.html', message="Error password different.")
    #revisar si ya esta el usuario
    if db.execute("SELECT username FROM users where username = :username", {"username": username}).rowcount != 0:
        return render_template("error.html", message = "Account already exits!")
    #generar cuenta
    db.execute("INSERT INTO users (username,password) VALUES (:a,:b)",{"a":username,"b":password})
    db.commit()
    return render_template('success.html', message="Success! You can log in now.")

@app.route("/login", methods=["POST","GET"])
def login():
    emailLogIn=request.form.get('emailLogIn')
    userPasswordLogIn=request.form.get('userPasswordLogIn')

    if db.execute("SELECT * FROM users WHERE username = :a",{"a":emailLogIn}).rowcount == 0:
        return render_template("error.html", message = "Wrong user or password")
    data = db.execute("SELECT * FROM users WHERE username = :a",{"a":emailLogIn}).fetchone()
    if data.username==emailLogIn and data.password==userPasswordLogIn:
        session["username"]=emailLogIn
        return render_template("main.html", name = session["username"])
    else:
        return render_template("error.html", message = "Wrong user or password")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/ideologia")
@login_required
def ideologia():
    return render_template("ideologia.html", name = session["username"])
@app.route("/personajes")
@login_required
def personajes():
    return render_template("personajes.html", name = session["username"])
@app.route("/contenido")
@login_required
def contenido():
    return render_template("contenido.html", name = session["username"])
