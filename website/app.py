import sys
from flask import Flask, redirect, render_template, request, jsonify # pip install flask
import jinja2 # pip install jinja2
import jsonutil
from flask_mqtt import Mqtt #pip install flask-mqtt
import json
from lib.dccpp import generateDccThrottleCmd, generateDccFunctionCmd

app = Flask(__name__)
app.static_folder = 'static'

sensors_values = {
    1: {
        "id": 1,
        "sensor": "RFID",
        "value": "3560"
    },
    2: {
        "id": 2,
        "sensor": "IR",
        "value": True
    }
}


app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = '' #and password Set this item when you need to verify username a
app.config['MQTT_PASSWORD'] = '' #and password Set this item when you need to verify username
app.config['MQTT_KEEPALIVE'] = 5000 # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False # If your broker supports TLS, set it True

mqtt_client = Mqtt()
mqtt_client.init_app(app)
topic_dcc = "pyui/dcc-K3xWvP4p4D"
topic_accessories = "pyui/accessories-9P5nN15kdp"

# Settings
debug_mode = False # Enable this to be able to view pages all pages without logging in

# Data
current_user = ""
admin_mode = False

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
    return render_template("home_page.html", current_user = current_user,admin_mode=admin_mode)

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
            print("Usuário inválido!") # Change to a popup later!
            return redirect(app.url_for('register_user'))

        for user in data['users']:
            if user['username'] == username:
                print("Usuário já cadastrado!") # Change to a popup later!
                return redirect(app.url_for('register_user'))

        data['users'].append({'username': username, 'password': password})
        jsonutil.export_json(app.root_path + '/database/credentials.json', data)
        return redirect(app.url_for('home_page')) # Redirect to list of users later
    else:
        print("Método inválido:", request.method)
        return redirect(app.url_for('register_user')) # ERRO!

@app.route('/register-user')
def register_user():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_user.html")

@app.route('/remove-user')
def remove_user():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("remove_user.html")

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
            return redirect(app.url_for('register_cab')) # Change to a popup later!

        cab_id = int(cab_id)

        for cab in data['cabs']:
            if int(cab['id']) == cab_id:
                print("Locomotiva já cadastrada!") # Change to a popup later!
                return redirect(app.url_for('register_cab'))
            
        data['cabs'].append({'id': cab_id, 'manufacturer': manufacturer, 'model': model})
        jsonutil.export_json(app.root_path + '/database/cabs.json', data)
        return redirect(app.url_for('home_page')) # Redirect to list of locomotives later
    else:
        print("Método inválido:", request.method)
        return redirect(app.url_for('register_cab')) # ERRO!

@app.route('/register-cab')
def register_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_cab.html")

@app.route('/remove-cab')
def remove_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("remove_cab.html")

# Handle CRUD for sensors

@app.route('/try-register-sensor', methods=['POST', 'GET'])
def try_register_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        name = request.form['name']
        value = request.form['value']
        data = jsonutil.import_json(app.root_path + '/database/sensors.json')

        if name.strip('') == "" or value.strip('') == "":
            print("Sensor inválido!")
            return redirect(app.url_for('register_sensor'))

        for sensor in data['sensors']:
            if sensor['name'] == name:
                print("Sensor já cadastrado!")
                return redirect(app.url_for('register_sensor')) # Change to a popup later!
        
        data['sensors'].append({'name': name, 'value': value})
        jsonutil.export_json(app.root_path + '/database/sensors.json', data)
        return redirect(app.url_for('home_page')) # Redirect to list of sensors later

@app.route('/register-sensor')
def register_sensor():
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

@app.route('/list-user')
def list_user():
  return render_template("list_user.html")

@app.route('/list-cab')
def list_cab():
  return render_template("list_cab.html")

@app.route('/list-sensor')
def list_sensor():
  return render_template("list_sensor.html")


# Handle MQTT
def publish_to_mqtt(topic, message):
    mqtt_client.publish(topic, message)

@app.route('/send_dcc_cmd', methods=['POST'])
def send_dcc_cmd():
    global topic_dcc

    data = request.get_json()

    cabId = data["cab"] or 3
    speed = data["speed"]
    direction = data["direction"]
    frontLight = data["frontLight"]
    secondaryLights = data["secondaryLight"]
    cmds = generateDccThrottleCmd(cabId, speed, direction) 
    cmds += generateDccFunctionCmd(cabId, frontLight, secondaryLights)

    publish_to_mqtt(topic_dcc, cmds)
    return ""

@app.route('/get_sensors_values', methods=['GET'])
def get_sensors_values():
    global sensors_values

    return jsonify(sensors_values)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Broker Connected successfully')
        mqtt_client.subscribe(topic_accessories)
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_disconnect()
def handle_disconnect(client, userdata, rc):
    print("Disconnected from broker")

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    global sensors_values

    data = json.loads(message.payload.decode())
    print(str(data))
    
    sensors_values[data["id"]] = data
    print(sensors_values)

app.run(debug = True)

