from flask import Flask, render_template # pip install flask
import jinja2 # pip install jinja2

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template("loginPage.html")

@app.route('/home')
def home_page():
    return render_template("homePage.html")

@app.route('/registerUser')
def register_user():
    return render_template("registerUser.html")

@app.route('/registerLocomotive')
def register_locomotive():
    return render_template("registerLocomotive.html")

@app.route('/registerSensor')
def register_sensor():
    return render_template("registerSensor.html")

@app.route('/removeUser')
def remove_user():
    return render_template("removeUser.html")

@app.route('/removeSensor')
def remove_sensor():
    return render_template("removeSensor.html")

@app.route('/removeLocomotive')
def remove_locomotive():
    return render_template("removeLocomotive.html")

app.run(debug=True)
