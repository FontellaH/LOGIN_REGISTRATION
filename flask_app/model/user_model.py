# make sure you match it to the users table in the database clip a snippet to reference too -->


from flask_app.config.mysqlconnection import connectToMySQL   # need a connection from mysqlconnection -->
from flask_app import DATABASE
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
ALPHA = re.compile(r"^[a-zA-Z]+$")


class User:                        
    def __init__(self, data) -> None:  #takes in data dictionary "__Init__"
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at =data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls, data):   # this login is to help me register/// whatever i pass into the %(key data) will get stored in the database
        query = """       
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    

    @classmethod
    def get_by_id(cls,data):  #getting by_id
        query = """
            SELECT * FROM users WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:    #if statement asking if i find the id return the results in the first index as a object
            return cls(results[0])
        return False   #otherwise return false.... THis is like a boolean check


    @classmethod
    def get_by_email(cls,data):   #getting_by_email
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:  #if statement asking for it to be return as a object in index 1
            return cls(results[0])
        return False   #otherwise return False
    

    @staticmethod     #Validating the form... /// Linked to register @app.route
    def is_valid(data):
        is_valid = True
#first_name validation
        if len(data['first_name']) < 1:
            flash('Fool... First name required', 'reg')
            is_valid = False
        elif len(data['first_name']) < 2:
            flash('Bro.. First name must be 2 characters at least', 'reg')
            is_valid = False
        elif not ALPHA.match(data['first_name']): 
            flash('Seriously.. First name can only contain letters', 'reg')
            is_valid = False
#last_name validation
        if len(data['last_name']) < 1:
            flash('Fool... Last name required', 'reg')
            is_valid = False
        elif len(data['last_name']) < 2:
            flash(' Bro.. Last name must be 2 characters at least', 'reg')
            is_valid = False
        elif not ALPHA.match(data['last_name']): 
            flash('Seriously.. Last name can only contain letters', 'reg')
            is_valid = False
#email validation 
        if len(data['email']) < 1:
            flash('First Attempt.. email required', 'reg')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash('Last Chance... email must be in proper format', 'reg')
            is_valid = False
        else:    
            potential_user = User.get_by_email({'email':data['email']}) #db is checking if email exist
            if potential_user:  #if it does exist it will flash
                flash('Dang GINA... email already exisits in db', 'reg')      
#password validation
        if len(data['password']) < 1:
            is_valid = False
            flash('This Again... password required', 'reg')
        elif len(data['password']) < 8:
            is_valid = False
            flash('Almost Got It... password must be 8 characters or more', 'reg')
        elif data['password'] != data['cpass']:   #if it dont match 
            is_valid = False 
            flash('20-min rule... password must match Get Help!', 'reg')  
        return is_valid    






    


