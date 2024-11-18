from flask import Blueprint, request, redirect, render_template, session, url_for
from utils.flask_utils import check_for_login
import utils.json_util
from utils.db_utils import start_query

detour_controller = Blueprint('detour_controller', __name__, template_folder="templates") 

# Handle CRUD for detours

@detour_controller.route('/try-remove-detour', methods=['POST', 'GET'])
def try_remove_detour():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        detour_id = request.form['detour_id']
        #data = utils.json_util.import_json(detour_controller.root_path + '/database/actuators.json')
        delete_id = int(start_query("SELECT * FROM turnout")[int(detour_id)][0])
        start_query(f"DELETE FROM turnout WHERE id = {delete_id}")
        print("O sensor foi removido com sucesso!")
        return redirect(url_for('detour_controller.list_detour'))

@detour_controller.route('/try-register-detour', methods=['POST', 'GET'])
def try_register_detour():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        detour_id = request.form['id']
        left_angle = request.form['left-angle']
        right_angle = request.form['right-angle']
        # data = utils.json_util.import_json(detour_controller.root_path + '/database/actuators.json')
        data = start_query("SELECT * FROM turnout")

        if detour_id.strip('') == "" or not detour_id.isnumeric() or not left_angle.isnumeric() or not right_angle.isnumeric():
            print("Desvio inválido!")
            return register_detour(error=True)

        print(data)
        for detour in data:
            if detour[0] == detour_id:
                print("Desvio já cadastrado!")
                return register_detour(error=True)
        
        start_query(f"INSERT INTO turnout (id, left_angle, right_angle) VALUES ({detour_id}, '{left_angle}', {right_angle})")
        return redirect(url_for('detour_controller.list_detour'))

@detour_controller.route('/try-edit-detour', methods=['POST', 'GET'])
def try_edit_detour():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        #print("\n"*100, request.form)
        edit_id = int(request.form['edit_id'])
        id = request.form['id']
        actuator = request.form['actuator']
        value = request.form['value']

        data = start_query("SELECT * FROM turnout")

        if id.strip('') == "" or actuator.strip('') == "" or value.strip('') == "" or not id.isnumeric() or not value.isnumeric():
            print("Sensor inválido!")
            return register_detour(error=True, data=[id, actuator, value], edit_id=edit_id)

        id = int(id)

        index = 0
        for sensor in data:
            if index != edit_id and int(sensor[0]) == id:
                print("Desvio já cadastrado!") 
                return register_detour(error=True, data=[id, actuator, value], edit_id=edit_id)
            index += 1
            
        start_query(f"DELETE FROM turnout WHERE id = {id}")
        start_query(f"INSERT INTO turnout (id, actuator, value) VALUES ({id}, '{actuator}', '{value}')")
        return redirect(url_for('detour_controller.list_detour')) # Redirect to list of locomotives later
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('detour_controller.register_detour')) # ERRO!


@detour_controller.route('/list-detour')
def list_detour():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    data = start_query("SELECT * FROM turnout")
    detours = {}
    index = 0
    for actuator in data:
        detours.update({index: actuator[0]})
        index += 1
    return render_template("list_detour.html", detours = detours)

@detour_controller.route('/register-detour')
def register_detour(error = False, data = ['', '', ''], edit_id = -1):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_detour.html", error = error, data=data, edit_id = edit_id)


@detour_controller.route('/edit-detour', methods=['POST', 'GET'])
def edit_detour(error = False):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        edit_id = request.form['edit_id']
        # data = utils.json_util.import_json(detour_controller.root_path + '/database/actuators.json')[int(edit_id)]
        data = start_query("SELECT * FROM turnout")
        data = data[int(edit_id)]
        return register_detour(error, [data[0], data[1], data[2]], int(edit_id))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('detour_controller.register_detour'))
