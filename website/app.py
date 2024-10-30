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

app = Flask(__name__)
app.static_folder = 'static'

app.register_blueprint(client, url_prefix='')
app.register_blueprint(user_blueprint, url_prefix='')
app.register_blueprint(cab_blueprint, url_prefix='')
app.register_blueprint(sensor_blueprint, url_prefix='')
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

# Handle CRUD for detours

@app.route('/try-remove-detour', methods=['POST', 'GET'])
def try_remove_detour():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        detour_id = request.form['detour_id']
        data = jsonutil.import_json(app.root_path + '/database/actuators.json')
        # print("\n\n\n\n\n\n\n\n\n\nSensor a ser removido:", sensor_id)
        name = data.pop(int(detour_id))
        jsonutil.export_json(app.root_path + '/database/actuators.json', data)
        print("O sensor", name, "foi removido com sucesso!")
        return redirect(app.url_for('list_detour'))

@app.route('/try-register-detour', methods=['POST', 'GET'])
def try_register_detour():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        detour_id = request.form['id']
        actuator = request.form['actuator']
        value = request.form['value']
        data = jsonutil.import_json(app.root_path + '/database/actuators.json')

        if actuator.strip('') == "" or not detour_id.isnumeric() or not value.isnumeric():
            print("Desvio inválido!")
            return register_detour(error=True)

        for detour in data:
            if detour['id'] == detour_id:
                print("Desvio já cadastrado!")
                return register_detour(error=True)
        
        data.append({'id': int(detour_id), 'actuator': actuator, 'value': int(value)})
        jsonutil.export_json(app.root_path + '/database/actuators.json', data)
        return redirect(app.url_for('list_detour'))

@app.route('/try-edit-detour', methods=['POST', 'GET'])
def try_edit_detour():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        #print("\n"*100, request.form)
        edit_id = int(request.form['edit_id']   )
        id = request.form['id']
        actuator = request.form['actuator']
        value = request.form['value']

        data = jsonutil.import_json(app.root_path + '/database/actuators.json')

        if id.strip('') == "" or actuator.strip('') == "" or value.strip('') == "" or not id.isnumeric() or not value.isnumeric():
            print("Sensor inválido!")
            return register_detour(error=True, data=[id, actuator, value], edit_id=edit_id)

        id = int(id)

        index = 0
        for sensor in data:
            if index != edit_id and int(sensor['id']) == id:
                print("Desvio já cadastrado!") 
                return register_detour(error=True, data=[id, actuator, value], edit_id=edit_id)
            index += 1
            
        data[edit_id] = {'id': int(id), 'actuator': actuator, 'value': int(value)}
        jsonutil.export_json(app.root_path + '/database/actuators.json', data)
        return redirect(app.url_for('list_detour')) # Redirect to list of locomotives later
    else:
        print("Método inválido:", request.method)
        return redirect(app.url_for('register_detour')) # ERRO!


@app.route('/list-detour')
def list_detour():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    data = jsonutil.import_json(app.root_path + '/database/actuators.json')
    detours = {}
    index = 0
    for actuator in data:
        detours.update({index: actuator['actuator']})
        #print('\n\n\n\n\n\n\n\n\n\n\n\n\n', actuator, " -:- ", detours)
        index += 1
    return render_template("list_detour.html", detours = detours)

@app.route('/register-detour')
def register_detour(error = False, data = ['', '', ''], edit_id = -1):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_detour.html", error = error, data=data, edit_id = edit_id)


@app.route('/edit-detour', methods=['POST', 'GET'])
def edit_detour(error = False):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        edit_id = request.form['edit_id']
        data = jsonutil.import_json(app.root_path + '/database/actuators.json')[int(edit_id)]
        return register_detour(error, [data['id'], data['actuator'], data['value']], int(edit_id))
    else:
        print("Método inválido:", request.method)
        return redirect(app.url_for('register_detour'))

app.run(debug=True)
