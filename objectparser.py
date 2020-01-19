from flask import jsonify

from models import *
import json


def getLanguagesList():
    with open('languages.json') as json_file:
        data = json.load(json_file)
    return data


def jsonToLanguage(json):
    return json.get('name'), json.get('full_name')


def addToLanguages(name, full_name):
    with open('languages.json') as file:
        data = json.load(file)
        for dat in data:
            if dat['name'] == name or dat['full_name'] == full_name:
                return
        data.append({
            "name": name,
            "full_name": full_name
        })
        with open('languages.json', 'w') as outfile:
            json.dump(data, outfile)


def jsonToUser(json):
    username = json.get('username')
    email = json.get('email')
    password = json.get('password')
    firstname = json.get('firstname')
    return User(xid=0, username=username, email=email, password=password, name=firstname)


def jsonToCategoryAndFiszki(json):
    name = json.get('name')
    src_lang = json.get('source_lang')
    target_lang = json.get('target_lang')
    jsons = json.get('fiszki')
    fiszki = []
    for js in jsons:
        src_text = js.get('src_text')
        target_text = js.get('target_text')
        fiszki.append(Fiszka(xid=0, category_id=0, src_text=src_text, target_text=target_text))
    category = Category(xid=0, user_id=0, name=name, src_lang=src_lang, target_lang=target_lang)
    return category, fiszki


def getUserResponse(user):
    return jsonify({"id": user.xid,
                    "username": user.username,
                    "email": user.email,
                    "firstname": user.name})


def createUserResponse(user_id):
    return jsonify({"id": user_id})


def createUserBadResponse(u, user):
    if u.email == user.email and u.username == user.username:
        return 'User with this email and username already exist.', 400
    if u.email == user.email:
        return 'User with this email already exist.', 400
    if u.username == user.username:
        return 'User with this username already exist.', 400
    return '', 400


def getCategoriesResponse(categories):
    response = []
    for category in categories:
        response.append({"id": category.xid,
                         "user_id": category.user_id,
                         "name": category.name,
                         "source_lang": category.src_lang,
                         "target_lang": category.target_lang})
    return jsonify(response)


def getFiszkiResponse(fiszki):
    response = []
    for fiszka in fiszki:
        response.append({"id": fiszka.xid,
                         "category_id": fiszka.category_id,
                         "source_text": fiszka.src_text,
                         "target_text": fiszka.target_text})
    return jsonify(response)


def createCategoryResponse(xid):
    return jsonify({"id": xid})
