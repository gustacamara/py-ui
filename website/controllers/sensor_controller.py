from flask import Blueprint, request, redirect, render_template, session, url_for
from utils.flask_utils import check_for_login
import utils.json_util

sensor_controller = Blueprint('sensor_controller', __name__, template_folder="templates") 

# Handle CRUD for sensors

@sensor_controller.route('/try-register-sensor', methods=['POST', 'GET'])
def try_register_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        sensor_id = request.form['id']
        name = request.form['name']
        value = request.form['value']
        data = utils.json_util.import_json(sensor_controller.root_path + '/database/sensors.json')

        if name.strip('') == "" or value.strip('') == "":
            print("Sensor inválido!")
            return redirect(url_for('sensor_controller.register_sensor'))

        for sensor in data:
            if sensor['id'] == sensor_id:
                print("Sensor já cadastrado!")
                return register_sensor(error=True)
        
        data.append({'id': sensor_id, 'sensor': name, 'value': value})
        utils.json_util.export_json(sensor_controller.root_path + '/database/sensors.json', data)
        return redirect(url_for('sensor_controller.list_sensor')) # Redirect to list of sensors later
    

@sensor_controller.route('/try-edit-sensor', methods=['POST', 'GET'])
def try_edit_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        #print("\n"*100, request.form)
        edit_id = int(request.form['edit_id']   )
        id = request.form['id']
        name = request.form['name']
        value = request.form['value']

        data = utils.json_util.import_json(sensor_controller.root_path + '/database/sensors.json')

        if id.strip('') == "" or name.strip('') == "" or value.strip('') == "" or not id.isnumeric():
            print("Sensor inválido!")
            return register_sensor(error=True, data=[id, name, value], edit_id=edit_id)

        id = int(id)

        index = 0
        for sensor in data:
            if index != edit_id and int(sensor['id']) == id:
                print("Sensor já cadastrado!") 
                return register_sensor(error=True, data=[id, name, value], edit_id=edit_id)
            index += 1
            
        data[edit_id] = {'id': id, 'sensor': name, 'value': value}
        utils.json_util.export_json(sensor_controller.root_path + '/database/sensors.json', data)
        return redirect(url_for('sensor_controller.list_sensor')) # Redirect to list of locomotives later
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('sensor_controller.register_sensor')) # ERRO!

@sensor_controller.route('/edit-sensor', methods=['POST', 'GET'])
def edit_sensor(error = False):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        sensor_id = request.form['sensor_id']
        data = utils.json_util.import_json(sensor_controller.root_path + '/database/sensors.json')[int(sensor_id)]
        return register_sensor(error, [data['id'], data['sensor'], data['value']], int(sensor_id))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('sensor_controller.register_sensor'))

@sensor_controller.route('/register-sensor')
def register_sensor(error = False, data = ['', '', ''], edit_id = -1):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_sensor.html", error = error, data=data, edit_id = edit_id)

@sensor_controller.route('/remove-sensor')
def remove_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("remove_sensor.html")

@sensor_controller.route('/list-sensor')
def list_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    data = utils.json_util.import_json(sensor_controller.root_path + '/database/sensors.json')
    sensors = {}
    index = 0
    for sensor in data:
        #print('\n\n\n\n\n\n\n\n\n\n\n\n\n', sensor)
        sensors.update({index: sensor['sensor']})
        index += 1
    return render_template("list_sensor.html", sensors = sensors)

@sensor_controller.route('/try-remove-sensor', methods=['POST', 'GET'])
def try_remove_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        sensor_id = request.form['sensor_id']
        data = utils.json_util.import_json(sensor_controller.root_path + '/database/sensors.json')
        # print("\n\n\n\n\n\n\n\n\n\nSensor a ser removido:", sensor_id)
        name = data.pop(int(sensor_id))
        utils.json_util.export_json(sensor_controller.root_path + '/database/sensors.json', data)
        print("O sensor", name, "foi removido com sucesso!")
        return redirect(url_for('sensor_controller.list_sensor'))