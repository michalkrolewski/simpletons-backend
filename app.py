from flask import Flask, request
from db.dbconnector import DBConnector
from flask_httpauth import HTTPBasicAuth
from objectparser import *
from werkzeug.security import generate_password_hash, check_password_hash
from utli import *
from os import environ
from flask_cors import CORS

app = Flask(__name__)
auth = HTTPBasicAuth()
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@auth.verify_password
def verify_password(username, password):
    db = DBConnector()
    user = db.getUserByUsername(username)
    if user is not None:
        return check_password_hash(user.password, password)
    return False


@app.route('/user', methods=['POST'])
def createUser():
    user = jsonToUser(request.json)
    db = DBConnector()
    u = db.getUserByUsernameOrEmail(user.username, user.email)
    if u is not None:
        return createUserBadResponse(u, user)
    user.password = generate_password_hash(user.password)
    user_id = db.createUser(user)
    return createUserResponse(user_id)


@app.route('/user/<int:user_id>', methods=['GET'])
@auth.login_required
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


@app.route('/category/public/<int:category_id>/fiszki', methods=['GET'])
@auth.login_required
def getPublicFiszki(category_id):
    db = DBConnector()
    categories = db.getPublicCategories()
    fiszki = {}
    for category in categories:
        if category.xid == category_id:
            fiszki = db.getFiszkiByCategory(category_id)

    return getFiszkiResponse(fiszki)


@app.route('/category/private/<int:category_id>/fiszki', methods=['GET'])
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


@app.route('/category', methods=['POST'])
@auth.login_required
def createCategory():
    category, fiszki = jsonToCategoryAndFiszki(request.json)
    userId = getLoggedUserId(auth.username())
    category.user_id = userId
    db = DBConnector()
    existingCategory = db.getCategory(userId, category.name)
    if existingCategory is None:
        existingCategory = db.createCategory(category)
    fillFiszkiWithCategoryId(fiszki, existingCategory.xid)
    db.createFiszki(fiszki)
    return createCategoryResponse(existingCategory.xid)


@app.route('/language', methods=['GET'])
@auth.login_required
def getLanguages():
    return jsonify(getLanguagesList())


@app.route('/language', methods=['POST'])
@auth.login_required
def addLanguage():
    name, full_name = jsonToLanguage(request.json)
    addToLanguages(name, full_name)
    return jsonify(getLanguagesList())


if __name__ == '__main__':
    # TODO: do uruchomienia na heroku - przed commitem odkomentowac te linie
    # app.run(host='0.0.0.0', port=environ.get("PORT", 5555))
    # TODO: do testowanie lokalnie - przed commitem zakomentowac
    app.run()
