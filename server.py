#import Flsk to sll us to creat our app
from flask_app import app  #attached to  __init__folder
from flask_app.controllers import users_controller





if __name__ == "__main__":   # Endure this file is running
    app.run(debug=True)       #Run this app to debug mode


