# __init__.py

from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh"

DATABASE = "login_registration"    #placed DATABASE here instead of in my ***_model.html file. get the correct file from the databse to run 