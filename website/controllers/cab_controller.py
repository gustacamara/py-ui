from flask import Blueprint, request, redirect, render_template, session, url_for
from utils.flask_utils import check_for_login
import utils.json_util
from utils.db_utils import start_query

cab_controller = Blueprint('cab_controller', __name__, template_folder="templates") 

# Handle CRUD for locomotives

@cab_controller.route('/try-register-cab', methods=['POST', 'GET'])
def try_register_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        #print(">>>>>>>>>>>>>>>form: ", request.form)
        cab_id = request.form['cab_id']
        manufacturer = request.form['manufacturer']
        model = request.form['model']

        data = start_query("SELECT * FROM cabs")

        if cab_id.strip('') == "" or manufacturer.strip('') == "" or model.strip('') == "" and cab_id.isnumeric():
            print("Locomotiva inválida!")
            return register_cab(error=True)

        cab_id = int(cab_id)

        for cab in data:
            if int(cab[0]) == cab_id:
                print("Locomotiva já cadastrada!") 
                return register_cab(error=True)
            
        data.append({'id': cab_id, 'manufacturer': manufacturer, 'model': model})
        start_query(f"INSERT INTO cabs (id, manufacturer, model) VALUES ({cab_id}, '{manufacturer}', '{model}')")
        return redirect(url_for('cab_controller.list_cab')) # Redirect to list of locomotives later
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('cab_controller.register_cab')) # ERRO!
    
    
@cab_controller.route('/try-edit-cab', methods=['POST', 'GET'])
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

        data = start_query("SELECT * FROM cabs")
        target = data[edit_id][0]

        if cab_id.strip('') == "" or manufacturer.strip('') == "" or model.strip('') == "" or not cab_id.isnumeric():
            print("Locomotiva inválida!")
            return register_cab(error=True, data=[cab_id, manufacturer, model], edit_id=edit_id) 

        cab_id = int(cab_id)

        index = 0
        for cab in data:
            if index != edit_id and int(cab[0]) == cab_id:
                print("Locomotiva já cadastrada!") 
                return register_cab(error=True, data=[cab_id, manufacturer, model], edit_id=edit_id)
            index += 1
            
        start_query(f"DELETE FROM cabs WHERE id = {target}")
        start_query(f"INSERT INTO cabs (id, manufacturer, model) VALUES ({cab_id}, '{manufacturer}', '{model}')")
        return redirect(url_for('cab_controller.list_cab')) # Redirect to list of locomotives later
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('cab_controller.register_cab')) # ERRO!

@cab_controller.route('/register-cab')
def register_cab(error = False, data = ['', '', ''], edit_id = -1):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_cab.html", error = error, data=data, edit_id = edit_id)

@cab_controller.route('/edit-cab', methods=['POST', 'GET'])
def edit_cab(error = False):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        edit_id = request.form['edit_id']
        data = start_query("select * from cabs")[int(edit_id)]
        # print('\n'*100, data)
        return register_cab(error, [data[0], data[1], data[2]], int(edit_id))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('cab_controller.register_cab'))

@cab_controller.route('/remove-cab')
def remove_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("remove_cab.html")

@cab_controller.route('/list-cab')
def list_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    data = start_query("SELECT * FROM cabs")
    # print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n',data)
    cabs = []

    for cab in data:
        cabs.append({ "id": cab[0], "manufacturer": cab[1], "model": cab[2] })

    return render_template("list_cab.html", cabs = cabs)

@cab_controller.route('/try-remove-cab', methods=['POST', 'GET'])
def try_remove_cab():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        cab_id = request.form['cab_id']
        # print("\n\n\n\n\n\n\n\n\n\nLocomotiva a ser removida:", cab_id)
        data = start_query("SELECT * FROM cabs")
        start_query(f"DELETE FROM cabs WHERE id = {data[int(cab_id)][0]}")
        print("Removida com sucesso!")
        return redirect(url_for('cab_controller.list_cab'))
