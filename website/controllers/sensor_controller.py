from flask import Blueprint, request, redirect, render_template, session, url_for
from utils.flask_utils import check_for_login
from utils.db_utils import start_query

sensor_controller = Blueprint('sensor_controller', __name__, template_folder="templates")

# Handle CRUD for sensors

@sensor_controller.route('/try-register-sensor', methods=['POST', 'GET'])
def try_register_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        sensor_id = request.form['id']
        location = request.form['location']
        sensor_type = request.form['type']
        data = start_query("SELECT * FROM sensor")

        sensor_type = int(sensor_type)

        if location.strip() == "" or location.strip() == "" or not sensor_id.isnumeric() or sensor_id.strip() == "":
            print("Sensor inválido!")
            return register_sensor(error=True)

        for sensor in data:
            if str(sensor[0]) == sensor_id:
                print("Sensor já cadastrado!")
                return register_sensor(error=True)

        start_query(f"INSERT INTO sensor (id, location, type) VALUES ({sensor_id}, '{location}', {sensor_type})")
        return redirect(url_for('sensor_controller.list_sensor'))

@sensor_controller.route('/try-edit-sensor', methods=['POST', 'GET'])
def try_edit_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        edit_id = int(request.form['edit_id'])
        id = request.form['id']
        location = request.form['location']
        sensor_type = request.form['type']

        sensor_type = int(sensor_type)

        data = start_query("SELECT * FROM sensor")

        if id.strip() == "" or location.strip() == "" or location.strip() == "" or not id.isnumeric():
            print("Sensor inválido!")
            return register_sensor(error=True, data=[id, location, sensor_type], edit_id=edit_id, selected=data[2])

        id = int(id)

        index = 0
        for sensor in data:
            if index != edit_id and int(sensor[0]) == id:
                print("Sensor já cadastrado!")
                return register_sensor(error=True, data=[id, location, sensor_type], edit_id=edit_id, selected=sensor_type)
            index += 1

        start_query(f"DELETE FROM sensor WHERE id = {data[edit_id][0]}")
        start_query(f"INSERT INTO sensor (id, location, type) VALUES ({id}, '{location}', {sensor_type})")
        return redirect(url_for('sensor_controller.list_sensor'))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('sensor_controller.register_sensor'))

@sensor_controller.route('/edit-sensor', methods=['POST', 'GET'])
def edit_sensor(error=False):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        sensor_id = request.form['sensor_id']
        data = start_query("SELECT * FROM sensor")
        data = data[int(sensor_id)]
        return register_sensor(error, [data[0], data[1], data[2]], int(sensor_id))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('sensor_controller.register_sensor'))

@sensor_controller.route('/register-sensor')
def register_sensor(error=False, data=['', '', ''], edit_id=-1, selected = 0):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_sensor.html", error=error, data=data, edit_id=edit_id, selected=selected)

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
    data = start_query("SELECT * FROM sensor")
    sensors = {}
    index = 0
    for sensor in data:
        sensors.update({index: sensor[1]})
        index += 1
    return render_template("list_sensor.html", sensors=sensors)

@sensor_controller.route('/try-remove-sensor', methods=['POST', 'GET'])
def try_remove_sensor():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        sensor_id = request.form['sensor_id']
        data = start_query("SELECT * FROM sensor")
        if int(sensor_id) < len(data):
            delete_id = data[int(sensor_id)][0]
            start_query(f"DELETE FROM sensor WHERE id = {delete_id}")
            print("O sensor foi removido com sucesso!")
        return redirect(url_for('sensor_controller.list_sensor'))
