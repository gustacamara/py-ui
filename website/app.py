import sys
from flask import Flask, redirect, render_template, request, jsonify # pip install flask
from flask_mqtt import Mqtt
import jinja2 # pip install jinja2
import jsonutil
from client import client, turnouts

app = Flask(__name__)
app.static_folder = 'static'

# Settings
debug_mode = True # Enable this to be able to view pages all pages without logging in

# Data
current_user = ""
admin_mode = False

app.register_blueprint(client)

def check_for_login():
    if not debug_mode and current_user == "":
        print("You must be logged!")
        return redirect(app.url_for('login_page', error=True))
    else:
        return None

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
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("home_page.html", current_user = current_user,admin_mode=admin_mode, turnouts = turnouts)

# Handle CRUD for users

@app.route('/try-register-user', methods=['POST', 'GET'])
def try_register_user():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = jsonutil.import_json(app.root_path + '/database/credentials.json')

        if username.strip(' ') == "" and password.strip(' ') == "":
            print("Usuário inválido!")
            return register_user(error=True)

        for user in data['users']:
            if user['username'] == username:
                print("Usuário já cadastrado!")
                return register_user(error=True)

        data['users'].append({'username': username, 'password': password})
        jsonutil.export_json(app.root_path + '/database/credentials.json', data)
        return redirect(app.url_for('list_user')) # Redirect to list of users later
    else:
        print("Método inválido:", request.method)
        return redirect(app.url_for('register_user')) # ERRO!

@app.route('/register-user')
def register_user(error = False):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_user.html", error = error)

@app.route('/remove-user')
def remove_user():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("remove_user.html")

@app.route('/try-remove-user', methods=['POST', 'GET'])
def try_remove_user():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        user_id = request.form['user_id']
        data = jsonutil.import_json(app.root_path + '/database/credentials.json')
        # print("\n\n\n\n\n\n\n\n\n\nUsuário a ser removido:", user_id)
        name = data['users'].pop(int(user_id))
        jsonutil.export_json(app.root_path + '/database/credentials.json', data)
        print("O usuário", name, "foi removido com sucesso!")
        return redirect(app.url_for('list_user')) # Redirect to list of users later

@app.route('/list-user')
def list_user():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    data = jsonutil.import_json(app.root_path + '/database/credentials.json')['users']
    admin_name = ''
    admin_id = 0
    users = {}
    index = 0
    for user in data:
        if index > 0:
            users.update({index: user['username']})
        else:
            admin_name = user['username']
        index += 1
    # print("\n\n\n\n\n\n\n\n\n\n\n\n\nUsuários:", users)
    return render_template("list_user.html", users = users, admin_name = admin_name, admin_id = admin_id)

# Handle CRUD for locomotives

@app.route('/try-register-cab', methods=['POST', 'GET'])
def try_register_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        #print(">>>>>>>>>>>>>>>form: ", request.form)
        cab_id = request.form['cab_id']
        manufacturer = request.form['manufacturer']
        model = request.form['model']

        data = jsonutil.import_json(app.root_path + '/database/cabs.json')

        if cab_id.strip('') == "" or manufacturer.strip('') == "" or model.strip('') == "":
            print("Locomotiva inválida!")
            return register_cab(error=True) 

        cab_id = int(cab_id)

        for cab in data['cabs']:
            if int(cab['id']) == cab_id:
                print("Locomotiva já cadastrada!") 
                return register_cab(error=True)
            
        data['cabs'].append({'id': cab_id, 'manufacturer': manufacturer, 'model': model})
        jsonutil.export_json(app.root_path + '/database/cabs.json', data)
        return redirect(app.url_for('list_cab')) # Redirect to list of locomotives later
    else:
        print("Método inválido:", request.method)
        return redirect(app.url_for('register_cab')) # ERRO!

@app.route('/register-cab')
def register_cab(error = False):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_cab.html", error = error)

@app.route('/remove-cab')
def remove_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("remove_cab.html")

@app.route('/list-cab')
def list_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    data = jsonutil.import_json(app.root_path + '/database/cabs.json')['cabs']
    # print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n',data)
    cabs = {}
    
    index = 0
    for cab in data:
        cabs.update({index: cab['id']})
        index += 1
    
    return render_template("list_cab.html", cabs = cabs)

@app.route('/try-remove-cab', methods=['POST', 'GET'])
def try_remove_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        cab_id = request.form['cab_id']
        data = jsonutil.import_json(app.root_path + '/database/cabs.json')
        # print("\n\n\n\n\n\n\n\n\n\nLocomotiva a ser removida:", cab_id)
        name = data['cabs'].pop(int(cab_id))
        jsonutil.export_json(app.root_path + '/database/cabs.json', data)
        print("A locomotiva", name, "foi removida com sucesso!")
        return redirect(app.url_for('list_cab'))

# Handle CRUD for sensors

@app.route('/try-register-sensor', methods=['POST', 'GET'])
def try_register_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        sensor_id = request.form['id']
        name = request.form['name']
        value = request.form['value']
        data = jsonutil.import_json(app.root_path + '/database/sensors.json')

        if name.strip('') == "" or value.strip('') == "":
            print("Sensor inválido!")
            return redirect(app.url_for('register_sensor'))

        for sensor in data:
            if sensor['id'] == sensor_id:
                print("Sensor já cadastrado!")
                return register_sensor(error=True)
        
        data.append({'id': sensor_id, 'sensor': name, 'value': value})
        jsonutil.export_json(app.root_path + '/database/sensors.json', data)
        return redirect(app.url_for('list_sensor')) # Redirect to list of sensors later

@app.route('/register-sensor')
def register_sensor(error = False):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_sensor.html")

@app.route('/remove-sensor')
def remove_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("remove_sensor.html")

@app.route('/list-sensor')
def list_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    data = jsonutil.import_json(app.root_path + '/database/sensors.json')
    sensors = {}
    index = 0
    for sensor in data:
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n', sensor)
        sensors.update({index: sensor['sensor']})
        index += 1
    return render_template("list_sensor.html", sensors = sensors)

@app.route('/try-remove-sensor', methods=['POST', 'GET'])
def try_remove_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        sensor_id = request.form['sensor_id']
        data = jsonutil.import_json(app.root_path + '/database/sensors.json')
        # print("\n\n\n\n\n\n\n\n\n\nSensor a ser removido:", sensor_id)
        name = data.pop(int(sensor_id))
        jsonutil.export_json(app.root_path + '/database/sensors.json', data)
        print("O sensor", name, "foi removido com sucesso!")
        return redirect(app.url_for('list_sensor'))

app.run(debug = True)

