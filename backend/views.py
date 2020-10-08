from backend import app
from flask import render_template, make_response

# load home page
@app.route('/')
def home():
    return 'Hello'



# load arbitrary static page
@app.route('/<string:page_name>/')
def load_page(page_name):
    return 'Hello ' + page_name

