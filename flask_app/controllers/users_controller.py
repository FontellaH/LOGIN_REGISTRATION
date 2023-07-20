from flask_app import app       #import app from my _init__

from flask import render_template, redirect, request, flash, session   #imported from my server.py

from flask_app.model.user_model import User   #*******<<< need to figure out why its not working *******

from flask_bcrypt import Bcrypt         # we are creating an object called bcrypt,
bcrypt = Bcrypt(app)          # which is made by invoking the function Bcrypt with our app as an argument




# @app.route('/')
# def index():
#     return render_template('index.html')


#In session
@app.route('/')
def index():     #if user is in session
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')


# Action route ↓↓↓
# Register Route..... To ***Validate**** the form.... write info in the user_model @staticmethod
@app.route('/users/register', methods=['POST'])
def register():
    if not User.is_valid(request.form):
        return redirect('/')   #If not vaild will redirect back to home('/') 
#if the password exist bcrypt will give the hashed password       
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data ={   #This is making a user by copying the request.form
        **request.form,
        'password' :hashed_pass,
        'cpass':hashed_pass  #this is not nessary but might make me feel safer
    }
    logged_user_id =User.create(data)  #creating a user to keep track of the user in session.. this is running the id # already installed in mysqlconnection
    session['user_id'] = logged_user_id   #storing user in session
    return redirect('/dashboard')


# Users Login... taking in a form so method is post
@app.route('/users/login', methods=['POST'])
def login():    #creating a email and pulling out from our requst.form the email that was applied
    data = {
        'email': request.form['email']
    }
    potential_user = User.get_by_email(data)
    if not potential_user:   #if the email is not in the data back you will get a flash
        flash('Invalid information', 'log')   #sending this to the login in section
        return redirect('/')   #redirecting them back to the home page
    if not bcrypt.check_password_hash(potential_user.password, request.form['password']):
        flash('Nope.... Invalid information', 'log')   #sending this to the login in section
        return redirect('/')   #redirecting them back to the home page 
    session['user_id'] = potential_user.id    #if working will send to dashboard
    return redirect('/dashboard')


# Log out.... 
@app.route('users/logout')
def logout():
    del session['user_id']
    return redirect('/')

# ******* Need to fix********



# Dashborad route/ Not in session
@app.route('/dashboard')  #making sure the user is logged in by looking for %()
def dashboard():
    if 'user_id' not in session:
        return redirect('/')  #if not in sssion will redirect to home ('/')
    data = {
        'id': session['user_id']  #calling the user to the database
    }
    logged_user = User.get_by_id(data)
    return render_template('dashboard.html', logged_user =logged_user)   #or render the name in dashboard


