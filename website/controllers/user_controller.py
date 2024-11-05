from flask import Blueprint, request, redirect, render_template, session, url_for
from utils.flask_utils import check_for_login
import utils.json_util

user_controller = Blueprint('user_blueprint', __name__, template_folder="templates") 

# Handle CRUD for users

@user_controller.route('/try-register-user', methods=['POST', 'GET'])
def try_register_user():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = utils.json_util.import_json(user_blueprint.root_path + '/database/credentials.json')

        if username.strip(' ') == "" and password.strip(' ') == "":
            print("Usuário inválido!")
            return register_user(error=True)

        for user in data['users']:
            if user['username'] == username:
                print("Usuário já cadastrado!")
                return register_user(error=True)

        data['users'].append({'username': username, 'password': password})
        utils.json_util.export_json(user_blueprint.root_path + '/database/credentials.json', data)
        return redirect(url_for('user_blueprint.list_user')) # Redirect to list of users later
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('user_blueprint.register_user')) # ERRO!
    
    
@user_controller.route('/try-edit-user', methods=['POST', 'GET'])
def try_edit_user():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        # print('\n'*100,request.form)
        username = request.form['username']
        password = request.form['password']
        data = utils.json_util.import_json(user_blueprint.root_path + '/database/credentials.json')

        print('n'*100, user_id, username, password)
        if username.strip(' ') == "" or password.strip(' ') == "":
            print("Usuário inválido!")
            return register_user(error=True, data=[username, password], edit_id=user_id)

        index = 0
        for user in data['users']:
            if index != user_id and user['username'] == username:
                print("Usuário já cadastrado!")
                return register_user(error=True, data=[username, password], edit_id=user_id)
            index += 1

        data['users'][user_id] = {'username': username, 'password': password}
        utils.json_util.export_json(user_blueprint.root_path + '/database/credentials.json', data)
        return redirect(url_for('user_blueprint.list_user'))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('register_user')) # ERRO!

@user_controller.route('/register-user')
def register_user(error = False, data = ['', ''], edit_id = -1):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("register_user.html", error = error, data=data, edit_id = edit_id)

@user_controller.route('/edit-user', methods=['POST', 'GET'])
def edit_user(error = False):
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        user_id = request.form['user_id']
        data = utils.json_util.import_json(user_blueprint.root_path + '/database/credentials.json')['users'][int(user_id)]
        return register_user(error, [data['username'], data['password']], int(user_id))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('register_user'))

@user_controller.route('/remove-user')
def remove_user():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    return render_template("remove_user.html")

@user_controller.route('/try-remove-user', methods=['POST', 'GET'])
def try_remove_user():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    if request.method == 'POST':
        user_id = request.form['user_id']
        data = utils.json_util.import_json(user_blueprint.root_path + '/database/credentials.json')
        # print("\n\n\n\n\n\n\n\n\n\nUsuário a ser removido:", user_id)
        name = data['users'].pop(int(user_id))
        utils.json_util.export_json(user_blueprint.root_path + '/database/credentials.json', data)
        print("O usuário", name, "foi removido com sucesso!")
        return redirect(url_for('user_blueprint.list_user')) # Redirect to list of users later

@user_controller.route('/list-user')
def list_user():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    data = utils.json_util.import_json(user_blueprint.root_path + '/database/credentials.json')['users']
    admin_name = ''
    admin_id = 0
    users = {}
    index = 0
    for user in data:
        if index > 0:
            users.update({index: user['username']})
        else:
            admin_name = user['username']
        index += 1
    # print("\n\n\n\n\n\n\n\n\n\n\n\n\nUsuários:", users)
    return render_template("list_user.html", users = users, admin_name = admin_name, admin_id = admin_id)