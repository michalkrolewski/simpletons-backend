from flask import Flask, request, Response
from os import environ
from db.dbconnector import DBConnector
from flask_httpauth import HTTPBasicAuth
from objectparser import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    db = DBConnector()
    user = db.getUserByUsername(username)
    if user is not None:
        return check_password_hash(user.password, password)
    return False

@app.route('/')
def hello_world():
    return "Hello world"


@app.route('/user', methods=['POST'])
def createUser():
    user = jsonToUser(request.json)
    user.password = generate_password_hash(user.password)
    db = DBConnector()
    user_id = db.createUser(user)
    return createUserResponse(user_id)


@app.route('/user/<int:user_id>', methods=['GET'])
def getUserById(user_id):
    db = DBConnector()
    user = db.getUserById(user_id)
    return getUserResponse(user)


@app.route('/user', methods=['GET'])
@auth.login_required
def getLoggedUserData():
    db = DBConnector()
    user = db.getUserByUsername(auth.username())
    return getUserResponse(user)


@app.route('/category/public', methods=['GET'])
def getPublicCategories():
    db = DBConnector()
    categories = db.getPublicCategories()
    return getCategoriesResponse(categories)


@app.route('/category/private', methods=['GET'])
@auth.login_required
def getPrivateCategories():
    userid = getLoggedUserId(auth.username())
    db = DBConnector()
    categories = db.getPrivateCategories(userid)
    return getCategoriesResponse(categories)


@app.route('/category/public/<int:category_id>', methods=['GET'])
def getPublicFiszki(category_id):
    db = DBConnector()
    categories = db.getPublicCategories()
    fiszki = {}
    for category in categories:
        if category.xid == category_id:
            fiszki = db.getFiszkiByCategory(category_id)

    return getFiszkiResponse(fiszki)


@app.route('/category/private/<int:category_id>', methods=['GET'])
@auth.login_required
def getPrivateFiszki(category_id):
    userid = getLoggedUserId(auth.username())
    db = DBConnector()
    categories = db.getPrivateCategories(userid)
    fiszki = {}
    for category in categories:
        if category.xid == category_id:
            fiszki = db.getFiszkiByCategory(category_id)

    return getFiszkiResponse(fiszki)


def getLoggedUserId(username):
    db = DBConnector()
    return db.getUserByUsername(username).xid;



if __name__ == '__main__':
    # TODO: do uruchomienia na heroku - przed commitem odkomentowac te linie
    # app.run(host='0.0.0.0', port=environ.get("PORT", 5555))
    # TODO: do testowanie lokalnie - przed commitem zakomentowac
    app.run()
