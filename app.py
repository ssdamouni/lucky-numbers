from flask import Flask, render_template, redirect, request, flash, jsonify
from random import randrange
import requests
from models import User, db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lucky_num'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)
db.create_all()

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")

@app.route("/api/get-lucky-num", methods=["POST"])
def  handle_user():
    user = User(name=request.json["name"], email=request.json["email"], year=request.json["year"] or 0, color=request.json['color'], rand_num=randrange(100))
    if user.check_info() == False:
        db.session.add(user)
        db.session.commit()
        
        response = {}
        num_request = requests.get(f'http://numbersapi.com/{user.rand_num}')
        num_dict = {"fact": f"{num_request.text}", "num": f"{user.rand_num}"}
        year_request = requests.get(f'http://numbersapi.com/{user.year}/year')
        year_dict = {"fact": f"{year_request.text}", "num": f"{user.year}"}

        response["num"] = num_dict
        response["year"] = year_dict

        return (jsonify(response), 201)
        #return (jsonify(user=user.serialize_users()), 201)
    else:
        return (jsonify(user.check_info()), 202)
