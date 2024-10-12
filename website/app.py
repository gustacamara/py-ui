import sys
from flask import Flask, redirect, render_template, request # pip install flask
import jinja2 # pip install jinja2
import jsonutil

app = Flask(__name__)
app.static_folder = 'static'

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

# Handle Crud for users

@app.route('/try-register-user', methods=['POST', 'GET'])
def try_register_user():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = jsonutil.import_json(app.root_path + '/database/credentials.json')

        if username.strip(' ') == "":
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

# Handle Crud for locomotives

@app.route('/try-register-cab', methods=['POST', 'GET'])
def try_register_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        #print(">>>>>>>>>>>>>>>form: ", request.form)
        cab_id = int(request.form['cab_id'])
        manufacturer = request.form['manufacturer']
        model = request.form['model']

        data = jsonutil.import_json(app.root_path + '/database/cabs.json')

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

# Handle Crud for sensors

@app.route('/try-register-sensor', methods=['POST', 'GET'])
def try_register_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        name = request.form['name']
        value = request.form['value']
        data = jsonutil.import_json(app.root_path + '/database/sensors.json')

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

app.run(debug=True)
