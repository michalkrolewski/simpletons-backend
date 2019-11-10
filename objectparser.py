from flask import jsonify

from models import *


def jsonToUser(json):
    username = json.get('username')
    email = json.get('email')
    password = json.get('password')
    firstname = json.get('firstname')
    return User(xid=0, username=username, email=email, password=password, name=firstname)


def jsonToCategoryAndFiszki(json):
    name = json.get('name')
    jsons = json.get('fiszki')
    fiszki = []
    for js in jsons:
        name = js.get('name')
        lang = js.get('lang')
        fiszki.append(Fiszka(xid=0, category_id=0, name=name, src_lang=lang))
    category = Category(xid=0, user_id=0, name=name)
    return category, fiszki


def getUserResponse(user):
    return jsonify({"id": user.xid,
                    "username": user.username,
                    "email": user.email,
                    "password": user.password,
                    "firstname": user.name})


def createUserResponse(user_id):
    return jsonify({"id": user_id})


def getCategoriesResponse(categories):
    response = []
    for category in categories:
        response.append({"id": category.xid,
                         "user_id": category.user_id,
                         "name": category.name})
    return jsonify(response)


def getFiszkiResponse(fiszki):
    response = []
    for fiszka in fiszki:
        response.append({"id": fiszka.xid,
                         "category_id": fiszka.category_id,
                         "language": fiszka.src_lang,
                         "text": fiszka.name})
    return jsonify(response)


def createCategoryResponse(xid):
    return jsonify({"id": xid})
