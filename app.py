from flask import Flask, request, Response
from os import environ
from db.dbconnector import DBConnector
from objectparser import *
from utli import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user', methods=['POST'])
def createUser():
    user = jsonToUser(request.json)
    db = DBConnector()
    user_id = db.createUser(user)
    return createUserResponse(user_id)


@app.route('/user/<int:user_id>', methods=['GET'])
def getUser(user_id):
    db = DBConnector()
    user = db.getUser(user_id)
    return getUserResponse(user)


@app.route('/category/public/all', methods=['GET'])
def getCategories():
    db = DBConnector()
    categories = db.getCategories()
    return getCategoriesResponse(categories)


@app.route('/fiszki/public', methods=['GET'])
def getFiszki():
    category_id = request.args.get('category_id')
    db = DBConnector()
    category = db.getCategory(category_id)
    if isPublic(category):
        return Response(status=400, response="Category is private!")

    fiszki = db.getFiszkiByCategory(category_id)
    return getFiszkiResponse(fiszki)


@app.route('/category', methods=['POST'])
def createCategory():
    category, fiszki = jsonToCategoryAndFiszki(request.json)
    category.user_id = 1  # TODO: ustawienie id zalogowanego uzytkownika
    db = DBConnector()
    xid = db.createCategory(category)
    fillFiszkiWithCategoryId(fiszki, xid)
    db.createFiszki(fiszki)
    return createCategoryResponse(xid)


if __name__ == '__main__':
    # TODO: do uruchomienia na heroku - przed commitem odkomentowac te linie
    app.run(host='0.0.0.0', port=environ.get("PORT", 5555))
    # TODO: do testowanie lokalnie - przed commitem zakomentowac
    # app.run()
