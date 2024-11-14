import sys
from flask import Flask, redirect, render_template, request, jsonify # pip install flask
from flask_mqtt import Mqtt
import jinja2 # pip install jinja2
import jsonutil
from client import client, turnouts, init_mqtt
from flask_utils import check_for_login

from user_blueprint import user_blueprint
from cab_blueprint import cab_blueprint
from sensor_blueprint import sensor_blueprint
from detour_blueprint import detour_blueprint

app = Flask(__name__)
app.static_folder = 'static'

app.config['DEBUG_MODE'] = False  # Enable this to be able to view pages without logging in
app.config['ADMIN_MODE'] = False
app.config['CURRENT_USER'] = ""  

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
    username = request.form['username']
    password = request.form['password']
    data = jsonutil.import_json(app.root_path + '/database/credentials.json')

    index = 0
    for user in data['users']:
        if user['username'] == username and user['password'] == password:
            app.config['CURRENT_USER'] = user['username']
            app.config['ADMIN_MODE'] = app.config['CURRENT_USER'] == data['users'][0]['username']
            return redirect(app.url_for('home_page'))
        index += 1
    print("Login inválido! tente novamente.")
    return login_page(error=True)

# Homepage

@app.route('/homepage')
def home_page():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    print("Current user:", app.config['CURRENT_USER'], "Admin mode:", app.config['ADMIN_MODE'])
    return render_template("home_page.html", current_user = app.config['CURRENT_USER'],admin_mode=app.config['ADMIN_MODE'], turnouts = turnouts)

@app.route('/about')
def about_page():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("about_page.html", current_user = app.config['CURRENT_USER'],admin_mode=app.config['ADMIN_MODE'])
app.run(debug=True)
