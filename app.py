from flask import Flask, request

from db.dbconnector import DBConnector
from objectparser import *

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


if __name__ == '__main__':
    app.run()
