from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
# Have import from mysqlconnection on every model for DB interactions
# Import the model's python file as a module, not the class directly so you avoid circular import errors!
# For example: from flask_app.models import table2_model

'''
! Note: If you are working with tables that are related to each other, 
!       you'll want to import the other table's class here for when you need to create objects with that class. 

! Example: importing pets so we can make pet objects for our users that own them.

Class should match the data table exactly that's in your DB.

REMEMBER TO PARSE DATA INTO OBJECTS BEFORE SENDING TO PAGES!

'''

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB= "login_schema"

    def __init__(self, data) -> None:
        self.id         = data[ "id"         ]
        self.first_name = data[ "first_name" ]
        self.last_name  = data[ "last_name"  ]
        self.email      = data[ "email"      ]
        self.password    = data[ "password"   ]
        self.created_at = data[ "created_at" ]
        self.updated_at = data[ "updated_at" ]

    @staticmethod
    def user_validate(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('Must be at least 2 characters.')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Must be at least 2 characters.')
            is_valid = False
        if len(user['email']) < 12:
            flash("Invalid email address!")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if user['password'] != user['confirm']:
            flash('Passwords did not match!')
            is_valid = False
        return is_valid

    @classmethod
    def add_user(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES(  %(first_name)s, %(last_name)s, %(email)s, %(password)s  );
        """

        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            flash('NOT a valid email/password!')
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return cls(result[0])
