
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import chore
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = "chore_schema" 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.chores = []



    # Create Users Models
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        result = connectToMySQL(cls.db).query_db(query,data)
        return result


    # Read Users Models
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_user_with_chores(cls, id):
        query = "SELECT * FROM users LEFT JOIN recipes ON chores.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('chore_schema').query_db(query, {"id":id} )
        # results will be a list of objects with the attached to each row. 
        user = cls(results[0])
        for row_from_db in results:
            # Now we parse the data to make instances and add them into our list.
            chore_data = {
                "id": row_from_db["chores.id"],
                "name": row_from_db["name"],
                "description": row_from_db["description"],
                "user_id": row_from_db["id"],
                "created_at": row_from_db["chores.created_at"],
                "updated_at": row_from_db["chores.updated_at"]
            }
            user.chores.append(chore.Chore( chore_data))
        return user

    @staticmethod
    def validate_user(user):
        is_valid = True # assume this is true
        if len(user['first_name']) < 2:
            flash("first name can't be less than 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("first name can't be less than 2 characters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("password can't be less than 8 characters")
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash("password doesn't match confirm password")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid