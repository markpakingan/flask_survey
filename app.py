from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)


responses = []

app.route('/')
def get_home():
    return render_template('base.html')