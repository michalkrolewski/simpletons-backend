from models import User


def parseUser(row):
    return User(row[0], row[1], row[2], row[3], row[4])
