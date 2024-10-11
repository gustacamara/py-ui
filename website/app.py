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
        print(">>>>>>>>>>>>>>>form: ", request.form)
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
        return redirect(app.url_for('home_page')) # Later redirect to list of users
    else:
        print("Método inválido:", request.method)
        return redirect(app.url_for('register_user')) # ERRO!

@app.route('/register-user')
def register_user():
    return render_template("register_user.html")


@app.route('/register-locomotive')
def register_locomotive():
    return render_template("register_locomotive.html")

@app.route('/register-sensor')
def register_sensor():
    return render_template("register_sensor.html")

@app.route('/remove-user')
def remove_user():
    return render_template("remove_user.html")

@app.route('/remove-sensor')
def remove_sensor():
    return render_template("remove_sensor.html")

@app.route('/remove-locomotive')
def remove_locomotive():
    return render_template("remove_locomotive.html")

app.run(debug=True)
