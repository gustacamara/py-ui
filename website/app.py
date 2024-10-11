import sys
from flask import Flask, redirect, render_template, request # pip install flask
import jinja2 # pip install jinja2
import jsonutil

app = Flask(__name__)
app.static_folder = 'static'

# Data
current_user = ""
admin_mode = False

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
            if index == 0:
                global admin_mode
                admin_mode = True

            global current_user
            current_user = user
            return redirect(app.url_for('home_page'))
        index += 1
    print("Login inválido! tente novamente.")
    return login_page(error=True)



@app.route('/homepage')
def home_page():
    return render_template("home_page.html")

# Handle Crud for users

@app.route('/try-register-user', methods=['POST', 'GET'])
def try_register_user():
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
    return render_template("register_user.html")

@app.route('/remove-user')
def remove_user():
    return render_template("remove_user.html")

# Handle Crud for locomotives

@app.route('/try-register-locomotive', methods=['POST', 'GET'])
def try_register_locomotive():
    if request.method == 'POST':
        #print(">>>>>>>>>>>>>>>form: ", request.form)
        locomotive_id = request.form['locomotive_id']
        manufacturer = request.form['manufacturer']
        model = request.form['model']

        data = jsonutil.import_json(app.root_path + '/database/cabs.json')

        for cab in data['cabs']:
            if['id'] == locomotive_id:
                print("Locomotiva já cadastrada!") # Change to a popup later!
                return redirect(app.url_for('register_locomotive'))
            
        data['cabs'].append({'id': locomotive_id, 'manufacturer': manufacturer, 'model': model})
        jsonutil.export_json(app.root_path + '/database/cabs.json', data)
        return redirect(app.url_for('home_page')) # Redirect to list of locomotives later
    else:
        print("Método inválido:", request.method)
        return redirect(app.url_for('register_locomotive')) # ERRO!

@app.route('/register-locomotive')
def register_locomotive():
    return render_template("register_locomotive.html")

@app.route('/remove-locomotive')
def remove_locomotive():
    return render_template("remove_locomotive.html")

# Handle Crud for sensors

@app.route('/try-register-sensor', methods=['POST', 'GET'])
def try_register_sensor():
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
    return render_template("register_sensor.html")

@app.route('/remove-sensor')
def remove_sensor():
    return render_template("remove_sensor.html")

app.run(debug=True)
