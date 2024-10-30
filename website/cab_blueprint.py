from flask import Blueprint, request, redirect, render_template, session, url_for
from flask_utils import check_for_login
import jsonutil

cab_blueprint = Blueprint('cab_blueprint', __name__, template_folder="templates") 

# Handle CRUD for locomotives

@cab_blueprint.route('/try-register-cab', methods=['POST', 'GET'])
def try_register_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        #print(">>>>>>>>>>>>>>>form: ", request.form)
        cab_id = request.form['cab_id']
        manufacturer = request.form['manufacturer']
        model = request.form['model']

        data = jsonutil.import_json(cab_blueprint.root_path + '/database/cabs.json')

        if cab_id.strip('') == "" or manufacturer.strip('') == "" or model.strip('') == "" and cab_id.isnumeric():
            print("Locomotiva inválida!")
            return register_cab(error=True) 

        cab_id = int(cab_id)

        for cab in data['cabs']:
            if int(cab['id']) == cab_id:
                print("Locomotiva já cadastrada!") 
                return register_cab(error=True)
            
        data['cabs'].append({'id': cab_id, 'manufacturer': manufacturer, 'model': model})
        jsonutil.export_json(cab_blueprint.root_path + '/database/cabs.json', data)
        return redirect(url_for('cab_blueprint.list_cab')) # Redirect to list of locomotives later
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('cab_blueprint.register_cab')) # ERRO!
    
    
@cab_blueprint.route('/try-edit-cab', methods=['POST', 'GET'])
def try_edit_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        #print("\n"*100, request.form)
        edit_id = int(request.form['edit_id']   )
        cab_id = request.form['cab_id']
        manufacturer = request.form['manufacturer']
        model = request.form['model']

        data = jsonutil.import_json(cab_blueprint.root_path + '/database/cabs.json')

        if cab_id.strip('') == "" or manufacturer.strip('') == "" or model.strip('') == "" or not cab_id.isnumeric():
            print("Locomotiva inválida!")
            return register_cab(error=True, data=[cab_id, manufacturer, model], edit_id=edit_id) 

        cab_id = int(cab_id)

        index = 0
        for cab in data['cabs']:
            if index != edit_id and int(cab['id']) == cab_id:
                print("Locomotiva já cadastrada!") 
                return register_cab(error=True, data=[cab_id, manufacturer, model], edit_id=edit_id)
            index += 1
            
        data['cabs'][edit_id] = {'id': cab_id, 'manufacturer': manufacturer, 'model': model}
        jsonutil.export_json(cab_blueprint.root_path + '/database/cabs.json', data)
        return redirect(url_for('cab_blueprint.list_cab')) # Redirect to list of locomotives later
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('cab_blueprint.register_cab')) # ERRO!

@cab_blueprint.route('/register-cab')
def register_cab(error = False, data = ['', '', ''], edit_id = -1):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_cab.html", error = error, data=data, edit_id = edit_id)

@cab_blueprint.route('/edit-cab', methods=['POST', 'GET'])
def edit_cab(error = False):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        edit_id = request.form['edit_id']
        data = jsonutil.import_json(cab_blueprint.root_path + '/database/cabs.json')['cabs'][int(edit_id)]
        # print('\n'*100, data)
        return register_cab(error, [data['id'], data['manufacturer'], data['model']], int(edit_id))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('cab_blueprint.register_cab'))

@cab_blueprint.route('/remove-cab')
def remove_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("remove_cab.html")

@cab_blueprint.route('/list-cab')
def list_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    data = jsonutil.import_json(cab_blueprint.root_path + '/database/cabs.json')['cabs']
    # print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n',data)
    cabs = {}
    
    index = 0
    for cab in data:
        cabs.update({index: cab['id']})
        index += 1
    
    return render_template("list_cab.html", cabs = cabs)

@cab_blueprint.route('/try-remove-cab', methods=['POST', 'GET'])
def try_remove_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        cab_id = request.form['cab_id']
        data = jsonutil.import_json(cab_blueprint.root_path + '/database/cabs.json')
        # print("\n\n\n\n\n\n\n\n\n\nLocomotiva a ser removida:", cab_id)
        name = data['cabs'].pop(int(cab_id))
        jsonutil.export_json(cab_blueprint.root_path + '/database/cabs.json', data)
        print("A locomotiva", name, "foi removida com sucesso!")
        return redirect(url_for('cab_blueprint.list_cab'))
