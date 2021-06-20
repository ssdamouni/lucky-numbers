from flask_sqlalchemy import SQLAlchemy
from random import randrange
import sqlalchemy.types as types
import datetime


db = SQLAlchemy()

class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class User(db.Model):
    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<name={u.name} id={u.id} email={u.email} year={u.year} color={u.color}>"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.Text, nullable=False)
    rand_num = db.Column(db.Integer, nullable=True)

    def check_info(self):
        #check all the submitted information to see it is valid
        errors = {}

        #check name
        if self.name:
            print("good name!")
        else:
            errors["name"] =  ["This field is required."]
        
        #check email
        if self.email:
            print("great email!")
        else:
            errors["email"] =  ["This field is required."]
        
        #check colors
        colors = ["red", "orange", "blue", "green"]
        for color in colors:
            if color == self.color:
                del errors["color"]
                break
            else: errors["color"] = ["Invalid value, must be one of: red, green, orange, blue."]
        
        #check year
        if self.year:
            print("great year!")
        else:
            errors["year"] =  ["This field is required."]
            
        if int(self.year) < 1900 or int(self.year) > 2000:
            errors["year"] = ["Invalid value, must be between 1900 and 2000 inclusive."]

        if errors:
            return errors

        return False

    def serialize_users(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'year': self.year,
            'color': self.color
        }

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)