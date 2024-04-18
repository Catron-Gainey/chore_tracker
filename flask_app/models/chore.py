from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Chore:
    db = "chore_schema" 
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.location = data['location']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None


    @classmethod
    def save_chore(cls, data):
        query = """INSERT INTO chores (name, description, location, user_id,)
                VALUES (%(name)s, %(description)s, %(location)s, %(user_id)s,);"""
        result = connectToMySQL(cls.db).query_db(query,data)
        return result
    
    @classmethod
    def get_all_chores(cls):
        query = "SELECT * FROM chores;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('chores').query_db(query)
        # Create an empty list to append the instances
        chores = []
        # Iterate over the db results and create instances with cls.
        for chore in results:
            chores.append(cls(chore))
        return chores
    

    @classmethod
    def get_all_chores_with_user(cls):
        # Get all and their one associated User that created it
        query = "SELECT * FROM chores JOIN users ON chores.user_id = users.id;"
        results = connectToMySQL('chore_schema').query_db(query)
        all_chores = []
        for row in results:
            # Create a class instance from the information from each db row
            one_chore = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_chores_author_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            # Create the User class instance that's in the user.py model file
            author = user.User(one_chores_author_info)
            # Associate the class instance with the User class instance by filling in the empty creator attribute in the class
            one_chore.user = author
            # Append containing the associated User to your list
            all_chores.append(one_chore)
        return all_chores
    
    @classmethod
    def get_one_chore_with_user(cls, id):
        # Get all and their one associated User that created it
        query = "SELECT * FROM chores JOIN users ON chores.user_id = users.id WHERE chores.id = %(id)s;"
        results = connectToMySQL('chore_schema').query_db(query, {"id":id})
        all_chores = []
        for row in results:
            # Create a class instance from the information from each db row
            one_chore = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_chores_author_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            # Create the User class instance that's in the user.py model file
            author = user.User(one_chores_author_info)
            # Associate the class instance with the User class instance by filling in the empty creator attribute in the class
            one_chore.user = author
            # Append containing the associated User to your list
            all_chores.append(one_chore)
        return all_chores

    @classmethod
    def update_chore(cls,user_data):
        query = """UPDATE chores 
                SET name=%(name)s, description=%(description)s, location=%(location)s
                WHERE id = %(id)s
                ;"""
        return connectToMySQL(cls.db).query_db(query,user_data)
    
    @classmethod
    def delete_choree(cls, id):
        query  = "DELETE FROM chores WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, {"id":id})
        return result
    
    # @staticmethod
    # def validate_recipe(data):
    #     is_valid = True # assume this is true
    #     if len(data['name']) < 3:
    #         flash("Name can't be less than 3 characters.")
    #         is_valid = False
    #     if len(data['description']) < 3:
    #         flash("Description can't be less than 3 characters.")
    #         is_valid = False
    #     if len(data['instructions']) < 3:
    #         flash("Instructions can't be less than 3 characters.")
    #         is_valid = False
    #     if 'under_30' not in data:
    #         flash("under 30 field cant be blank.")
    #         is_valid = False
    #     if len(data['date_made']) < 1:
    #         flash("date made cant be blank")
    #         is_valid = False
    #     return is_valid