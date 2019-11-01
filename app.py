from flask import Flask
from models import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'



@app.route('/test')
def test():
    category = Category(1, 1, "name")
    return category.name


if __name__ == '__main__':
    app.run()
