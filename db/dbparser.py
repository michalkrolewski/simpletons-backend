from models import *


def parseUser(row):
    return User(row[0], row[1], row[2], row[3], row[4])


def parseCategories(rows):
    categories = []
    for row in rows:
        categories.append(Category(row[0], row[1], row[2]))
    return categories
