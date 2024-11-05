import sys
from flask import Flask, redirect, render_template, request, jsonify # pip install flask
from flask_mqtt import Mqtt
import jinja2 # pip install jinja2
import utils.json_util
from utils.db_utils import create_db
from client import client, turnouts, init_mqtt
from utils.flask_utils import check_for_login

from .user_controller import user_controller
from .cab_controller import cab_controller
from .sensor_controller import sensor_controller
from .detour_controller import detour_controller

def create_app():
    app = Flask(__name__,template_folder="./views/",static_folder="./static/", root_path="./")
    app.static_folder = 'static'
    
    db, cursor = create_db()

    app.config['DEBUG_MODE'] = False  # Enable this to be able to view pages without logging in
    app.config['ADMIN_MODE'] = False
    app.config['CURRENT_USER'] = ""  

    app.register_blueprint(client, url_prefix='')
    app.register_blueprint(user_controller, url_prefix='')
    app.register_blueprint(cab_controller, url_prefix='')
    app.register_blueprint(sensor_controller, url_prefix='')
    app.register_blueprint(detour_controller, url_prefix='')
    init_mqtt(app)



    # Handle login
    @app.route('/', methods=['POST', 'GET'])
    def login_page(error=False):
        return render_template("login_page.html", error=error)

    @app.route('/try_authenticate', methods=['POST'])
    def try_authenticate():
        username = request.form['username']
        password = request.form['password']
        data = utils.json_util.import_json(app.root_path + '/database/credentials.json')

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
    return app
