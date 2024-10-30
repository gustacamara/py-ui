from flask import current_app, redirect
from flask_data import current_user, debug_mode

def check_for_login(test=False):
    global current_user, debug_mode
    print("current_user:", current_user, "debug_mode:", debug_mode, "test:", test)
    if not debug_mode and current_user == "":
        print("You must be logged!")
        return redirect(current_app.url_for('login_page', error=True))
    else:
        return None