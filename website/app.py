import sys
from flask import Flask, redirect, render_template, request, jsonify # pip install flask
from flask_mqtt import Mqtt
import jinja2 # pip install jinja2
import jsonutil
from client import client, turnouts, init_mqtt
from flask_data import debug_mode, current_user, admin_mode
from flask_utils import check_for_login

from user_blueprint import user_blueprint
from cab_blueprint import cab_blueprint
from sensor_blueprint import sensor_blueprint
from detour_blueprint import detour_blueprint

app = Flask(__name__)
app.static_folder = 'static'

app.register_blueprint(client, url_prefix='')
app.register_blueprint(user_blueprint, url_prefix='')
app.register_blueprint(cab_blueprint, url_prefix='')
app.register_blueprint(sensor_blueprint, url_prefix='')
app.register_blueprint(detour_blueprint, url_prefix='')
init_mqtt(app)


# Handle login
@app.route('/', methods=['POST', 'GET'])
def login_page(error=False):
    return render_template("login_page.html", error=error)

@app.route('/try_authenticate', methods=['POST'])
def try_authenticate():
    global current_user, admin_mode
    username = request.form['username']
    password = request.form['password']
    data = jsonutil.import_json(app.root_path + '/database/credentials.json')

    index = 0
    for user in data['users']:
        if user['username'] == username and user['password'] == password:
            global current_user
            global admin_mode
            current_user = user['username']
            admin_mode = current_user == data['users'][0]['username']
            return redirect(app.url_for('home_page'))
        index += 1
    print("Login inválido! tente novamente.")
    return login_page(error=True)

# Homepage

@app.route('/homepage')
def home_page():
    global current_user, admin_mode, turnouts
    login_check = check_for_login()
    if login_check != None:
        return login_check
    print("Current user:", current_user, "Admin mode:", admin_mode)
    return render_template("home_page.html", current_user = current_user,admin_mode=admin_mode, turnouts = turnouts)

app.run(debug=True)
