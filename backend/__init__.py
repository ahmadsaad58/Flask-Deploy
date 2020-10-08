from flask import Flask 

# create app
app = Flask(__name__)

from backend import views
