from flask import Blueprint, request, redirect, render_template, session, url_for
from flask_utils import check_for_login
import jsonutil

detour_blueprint = Blueprint('detour_blueprint', __name__, template_folder="templates") 

# Handle CRUD for detours

@detour_blueprint.route('/try-remove-detour', methods=['POST', 'GET'])
def try_remove_detour():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        detour_id = request.form['detour_id']
        data = jsonutil.import_json(detour_blueprint.root_path + '/database/actuators.json')
        # print("\n\n\n\n\n\n\n\n\n\nSensor a ser removido:", sensor_id)
        name = data.pop(int(detour_id))
        jsonutil.export_json(detour_blueprint.root_path + '/database/actuators.json', data)
        print("O sensor", name, "foi removido com sucesso!")
        return redirect(url_for('detour_blueprint.list_detour'))

@detour_blueprint.route('/try-register-detour', methods=['POST', 'GET'])
def try_register_detour():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        detour_id = request.form['id']
        actuator = request.form['actuator']
        value = request.form['value']
        data = jsonutil.import_json(detour_blueprint.root_path + '/database/actuators.json')

        if actuator.strip('') == "" or not detour_id.isnumeric() or not value.isnumeric():
            print("Desvio inválido!")
            return register_detour(error=True)

        for detour in data:
            if detour['id'] == detour_id:
                print("Desvio já cadastrado!")
                return register_detour(error=True)
        
        data.append({'id': int(detour_id), 'actuator': actuator, 'value': int(value)})
        jsonutil.export_json(detour_blueprint.root_path + '/database/actuators.json', data)
        return redirect(url_for('detour_blueprint.list_detour'))

@detour_blueprint.route('/try-edit-detour', methods=['POST', 'GET'])
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

        data = jsonutil.import_json(detour_blueprint.root_path + '/database/actuators.json')

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
        jsonutil.export_json(detour_blueprint.root_path + '/database/actuators.json', data)
        return redirect(url_for('detour_blueprint.list_detour')) # Redirect to list of locomotives later
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('detour_blueprint.register_detour')) # ERRO!


@detour_blueprint.route('/list-detour')
def list_detour():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    data = jsonutil.import_json(detour_blueprint.root_path + '/database/actuators.json')
    detours = {}
    index = 0
    for actuator in data:
        detours.update({index: actuator['actuator']})
        #print('\n\n\n\n\n\n\n\n\n\n\n\n\n', actuator, " -:- ", detours)
        index += 1
    return render_template("list_detour.html", detours = detours)

@detour_blueprint.route('/register-detour')
def register_detour(error = False, data = ['', '', ''], edit_id = -1):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_detour.html", error = error, data=data, edit_id = edit_id)


@detour_blueprint.route('/edit-detour', methods=['POST', 'GET'])
def edit_detour(error = False):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        edit_id = request.form['edit_id']
        data = jsonutil.import_json(detour_blueprint.root_path + '/database/actuators.json')[int(edit_id)]
        return register_detour(error, [data['id'], data['actuator'], data['value']], int(edit_id))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('detour_blueprint.register_detour'))
