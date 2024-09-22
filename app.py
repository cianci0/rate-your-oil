from flask import Flask, render_template, request, redirect, session
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
        print(session["username"])
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    username = session.get("username")
    if not username:
        return redirect("/login")
    return render_template("dashboard.html", username=username)

@app.route("/rate")
def rate():
    return render_template("rate.html")

@app.route("/your-oils")
def your_oils():
    return render_template("your-oils.html")

@app.route("/best-oils")
def best_oils():
    return render_template("best-oils.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login") 