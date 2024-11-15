from flask import Blueprint, request, redirect, render_template, session, url_for
from utils.flask_utils import check_for_login
from utils.db_utils import create_db, start_query
import sqlite3

user_controller = Blueprint('user_controller', __name__, template_folder="templates") 

# Handle CRUD for users

@user_controller.route('/try-register-user', methods=['POST', 'GET'])
def try_register_user():
    login_check = check_for_login()
    if login_check is not None:
        return login_check
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username.strip() == "" or password.strip() == "":
            print("Usuário inválido!")
            return register_user(error=True)

        existing_user = start_query(f"SELECT * FROM users WHERE username = '{username}'")
        if existing_user:
            print("Usuário já cadastrado!")
            return register_user(error=True)

        start_query(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        return redirect(url_for('user_controller.list_user'))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('user_controller.register_user'))

@user_controller.route('/try-edit-user', methods=['POST', 'GET'])
def try_edit_user():
    login_check = check_for_login()
    if login_check is not None:
        return login_check

    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        username = request.form['username']
        password = request.form['password']

        if username.strip() == "" or password.strip() == "":
            print("Usuário inválido!")
            return register_user(error=True, data=[username, password], edit_id=user_id)

        existing_user = start_query(f"SELECT * FROM users WHERE username = '{username}' AND rowid != {user_id}")
        if existing_user:
            print("Usuário já cadastrado!")
            return register_user(error=True, data=[username, password], edit_id=user_id)
        
        start_query(f"UPDATE users SET username = '{username}', password = '{password}' WHERE rowid = {user_id}")
        return redirect(url_for('user_controller.list_user'))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('register_user'))

@user_controller.route('/register-user')
def register_user(error=False, data=['', ''], edit_id=-1):
    login_check = check_for_login()
    if login_check is not None:
        return login_check
    return render_template("register_user.html", error=error, data=data, edit_id=edit_id)

@user_controller.route('/edit-user', methods=['POST', 'GET'])
def edit_user(error=False):
    login_check = check_for_login()
    if login_check is not None:
        return login_check
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_data = start_query(f"SELECT username, password FROM users WHERE rowid = {int(user_id)}")
        if user_data:
            data = user_data[0]
            return register_user(error, [data[0], data[1]], int(user_id))
        else:
            print("Usuário não encontrado.")
            return redirect(url_for('user_controller.list_user'))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('register_user'))

@user_controller.route('/remove-user')
def remove_user():
    login_check = check_for_login()
    if login_check is not None:
        return login_check
    return render_template("remove_user.html")

@user_controller.route('/try-remove-user', methods=['POST', 'GET'])
def try_remove_user():
    login_check = check_for_login()
    if login_check is not None:
        return login_check
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_data = start_query(f"SELECT username FROM users WHERE rowid = {int(user_id)}")
        if user_data:
            start_query(f"DELETE FROM users WHERE rowid = {int(user_id)}")
            print(f"O usuário {user_data[0][0]} foi removido com sucesso!")
            return redirect(url_for('user_controller.list_user'))
        else:
            print("Usuário não encontrado.")
            return redirect(url_for('user_controller.list_user'))
    else:
        print("Método inválido:", request.method)
        return redirect(url_for('register_user'))

@user_controller.route('/list-user')
def list_user():
    login_check = check_for_login()
    if login_check is not None:
        return login_check
    data = start_query("SELECT rowid, username FROM users")
    users = {row[0]: row[1] for row in data}
    admin_name = users.pop(1, '')
    admin_id = 1  
    return render_template("list_user.html", users=users, admin_name=admin_name, admin_id=admin_id)
