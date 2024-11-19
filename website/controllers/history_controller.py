from flask import Blueprint, request, redirect, render_template, session, url_for
from utils.flask_utils import check_for_login
from utils.db_utils import start_query

history_controller = Blueprint('history_controller', __name__, template_folder="templates")

# Handle CRUD for sensors

@history_controller.route('/history')
def list_history():
    login_check = check_for_login()
    if login_check != None:
        return login_check
    data = start_query("SELECT * FROM sensors_history")
    print('\n'*100, data)

    return render_template("history_page.html", history=data)