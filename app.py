from flask import Flask, render_template, request
from utils.functions import verifyPass, writePass, resetPass, verifyEmail


app = Flask(__name__, template_folder = "templates")

@app.route('/login/', methods =["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        if verifyPass(email, password):
            return render_template('success.html')
    return render_template('login.html')

@app.route('/signin/', methods =["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        confirmPass = request.form.get("conf-pass")
        if confirmPass == password and not verifyEmail(email):
            writePass(email, password)
            return render_template('success.html')
    return render_template('signin.html')

@app.route('/reset/', methods =["GET", "POST"])
def reset():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        confirmPass = request.form.get("conf-pass")
        if confirmPass == password and verifyEmail(email):
            resetPass(email, password)
            return render_template('success.html')
    return render_template('reset.html')

if __name__ == "__main__":
    app.run()