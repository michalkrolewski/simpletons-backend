class User:
    def __init__(self, xid, username, email, password, name):
        self.xid = xid
        self.username = username
        self.email = email
        self.password = password
        self.name = name

    def __str__(self):
        return '\'' + self.username + "\',\'" + self.email + "\',\'" + self.password + "\',\'" + self.name + "\'"


class Category:
    def __init__(self, xid, user_id, name, src_lang, target_lang):
        self.xid = xid
        self.user_id = user_id
        self.name = name
        self.src_lang = src_lang
        self.target_lang = target_lang

    def __str__(self):
        return '\'' + str(self.user_id) + "\',\'" + self.name + "','" + self.src_lang + "','" + self.target_lang + "'"


class Fiszka:
    def __init__(self, xid, category_id, src_text, target_text):
        self.xid = xid
        self.category_id = category_id
        self.src_text = src_text
        self.target_text = target_text

    def __str__(self):
        return "('" + str(
            self.category_id) + "','" + self.src_text + "','" + self.target_text + "')"
