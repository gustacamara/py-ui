from flask import current_app, redirect

def check_for_login(test=False):
    if not current_app.config['DEBUG_MODE'] and current_app.config['CURRENT_USER'] == "":
        print("You must be logged!")
        return redirect(current_app.url_for('login_page', error=True))
    else:
        return None