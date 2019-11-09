from flask import jsonify

from models import *


def jsonToUser(json):
    username = json.get('username')
    email = json.get('email')
    password = json.get('password')
    firstname = json.get('firstname')
    return User(xid=0, username=username, email=email, password=password, name=firstname)


def getUserResponse(user):
    return jsonify({"id": user.xid,
                    "username": user.username,
                    "email": user.email,
                    "password": user.password,
                    "firstname": user.name})


def createUserResponse(user_id):
    return jsonify({"id": user_id})
