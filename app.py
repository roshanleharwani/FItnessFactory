from flask import Flask, render_template, request, redirect, flash, session
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import json
from flask_mail import Mail, Message
import requests

app = Flask(__name__)

with open("config.json") as file:
    data = json.load(file)
    params = data["params"]


# MongoDB Setup
uri = "mongodb+srv://roshanleharwani:kYBdCTFNi3u6ktif@users.lo1ne1j.mongodb.net/?retryWrites=true&w=majority&appName=Users"
client = MongoClient(uri)
db = client.users

# Flask Configurations
app.config["SECRET_KEY"] = "secret_key"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = params["email"] 
app.config["MAIL_PASSWORD"] = params["pass"]   
app.config["MAIL_DEFAULT_SENDER"] = params["email"]  

mail = Mail(app)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return render_template("main.html",name=name)

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = db.users.find_one({"email": email})
        name = user.get('name')
        if user:
            if bcrypt.check_password_hash(user.get("password"), password):
                session["user"] = email
                flash("Success alert! You have Logged in successfully")
                return render_template("main.html",name=name)
            else:
                flash("Invalid Credentials !!  ")
                return redirect(request.url)
        else:
            flash("User Does not exist !!  ")
            return redirect(request.url)

    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        dob = request.form.get("dob")
        if name and email and phone and password and password:
            password = bcrypt.generate_password_hash(password).decode("utf-8")
            db.users.insert_one(
                {
                    "name": name,
                    "phone": phone,
                    "dob": dob,
                    "email": email,
                    "password": password,
                }
            )
            flash("Success alert! You have Signed UP successfully ")
            session["user"] = email
            return render_template("main.html",name=name)
        else:
            flash("All Fields are required")
            return render_template("signup.html")
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Info alert! You have Logged Out Successfully  ")
    return redirect("/")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        email = request.form.get("email")
        subject = request.form.get("subject")
        msg = request.form.get("message")
        message = Message(subject=subject, recipients=[params["email"]])
        message.body = f"{msg}\n\nEmail: {email}"
        mail.send(message)
        return render_template('index.html')
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
