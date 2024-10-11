import sys
from flask import Flask, redirect, render_template, request # pip install flask
import jinja2 # pip install jinja2
import jsonutil

app = Flask(__name__)
app.static_folder = 'static'

# Data
current_user = ""
admin_mode = False


@app.route('/', methods=['POST', 'GET'])
def login_page(error=False):
    return render_template("login_page.html", error=error)

@app.route('/try_authenticate', methods=['POST'])
def try_authenticate():
    username = request.form['username']
    password = request.form['password']
    data = jsonutil.import_json(app.root_path + '/database/credentials.json')

    index = 0
    for user in data['users']:
        if user['username'] == username and user['password'] == password:
            if index == 0:
                global admin_mode
                admin_mode = True

            global current_user
            current_user = user
            return redirect(app.url_for('home_page'))
        index += 1
    print("Login inválido! tente novamente.")
    return login_page(error=True)



@app.route('/homePage')
def home_page():
    return render_template("home_page.html")

@app.route('/registerUser')
def register_user():
    return render_template("register_user.html")

@app.route('/registerLocomotive')
def register_locomotive():
    return render_template("register_locomotive.html")

@app.route('/registerSensor')
def register_sensor():
    return render_template("register_sensor.html")

@app.route('/removeUser')
def remove_user():
    return render_template("remove_user.html")

@app.route('/removeSensor')
def remove_sensor():
    return render_template("remove_sensor.html")

@app.route('/removeLocomotive')
def remove_locomotive():
    return render_template("remove_locomotive.html")

app.run(debug=True)
