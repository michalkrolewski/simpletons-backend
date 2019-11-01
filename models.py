class User:
    def __init__(self, xid, username, email, password, name):
        self.xid = xid
        self.username = username
        self.email = email
        self.password = password
        self.name = name


class Category:
    def __init__(self, xid, user_id, name):
        self.xid = xid
        self.user_id = user_id
        self.name = name


class Fiszka:
    def __init__(self, xid, category_id, name, src_lang):
        self.xid = xid
        self.category_id = category_id
        self.name = name
        self.src_lang = src_lang
