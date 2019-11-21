from models import *


def parseUser(row):
    return User(row[0], row[1], row[2], row[3], row[4])


def parseCategories(rows):
    categories = []
    for row in rows:
        categories.append(parseCategory(row))
    return categories


def parseCategory(row):
    return Category(row[0], row[1], row[2])


def parseFiszki(rows):
    fiszki = []
    for row in rows:
        fiszki.append(Fiszka(row[0], row[1], row[2], row[3], row[4], row[5]))
    return fiszki
