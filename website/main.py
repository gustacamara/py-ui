from flask import Flask, render_template # pip install flask
import jinja2 # pip install jinja2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("loginPage.html")

@app.route('/home')
def home_page():
    return render_template("homePage.html")

app.run(debug=True)
